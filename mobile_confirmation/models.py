from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

import string,random

from .exceptions import (
    MobileConfirmationExpired, MobileIsPrimary, MobileNotConfirmed,
)
from .signals import (
    mobile_confirmed, unconfirmed_mobile_created, primary_mobile_changed,
)


class UserMobileConfirmation(object):
    """
    Mixin to be used with your django 1.5+ custom User model.
    Provides python-level functionality only.
    """

    # if your User object stores the User's primary mobile number
    # in a place other than User.mobile, you can override the
    # primary_mobile_field_name and/or primary_mobile get/set methods.
    # All access to a User's primary_mobile in this app passes through
    # these two get/set methods.

    primary_mobile_field_name = 'mobile'

    def get_primary_mobile(self):
        return getattr(self, self.primary_mobile_field_name)

    def set_primary_mobile(self, email, require_confirmed=True):
        "Set an mobile number as primary"
        old_mobile = self.get_primary_mobile()
        if mobile == old_mobile:
            return

        if mobile not in self.confirmed_mobiles and require_confirmed:
            raise MobileNotConfirmed()

        setattr(self, self.primary_mobile_field_name, mobile)
        self.save(update_fields=[self.primary_mobile_field_name])
        primary_mobile_changed.send(
            sender=self, old_mobile=old_mobile, new_mobile=mobile,
        )

    @property
    def is_confirmed(self):
        "Is the User's primary mobile number confirmed?"
        return self.get_primary_mobile() in self.confirmed_mobiles

    @property
    def confirmed_at(self):
        "When the User's primary mobile number was confirmed, or None"
        numbers = self.mobile_numbers_set.get(mobile=self.get_primary_mobile())
        return numbers.confirmed_at

    @property
    def mobile_confirmation_key(self):
        """
        Confirmation key for the User's primary mobile

        DEPRECATED. Use get_confirmation_key() instead.
        """
        mobile = self.get_primary_mobile()
        return self.get_mobile_confirmation_key(mobile)

    @property
    def confirmed_mobiles(self):
        "DEPRECATED. Use get_confirmed_mobiles() instead."
        return self.get_confirmed_mobiles()

    @property
    def unconfirmed_mobiles(self):
        "DEPRECATED. Use get_unconfirmed_mobiles() instead."
        return self.get_unconfirmed_mobiles()

    def get_mobile_confirmation_key(self, mobile=None):
        "Get the confirmation key for an mobile"
        mobile = mobile or self.get_primary_mobile()
        numbers = self.mobile_numbers_set.get(mobile=mobile)
        return numbers.key

    def get_confirmed_mobiles(self):
        "List of mobiles this User has confirmed"
        numbers_qs = self.mobile_numbers_set.filter(confirmed_at__isnull=False)
        return [numbers.mobile for numbers in numbers_qs]

    def get_unconfirmed_mobiles(self):
        "List of mobiles this User has been associated with but not confirmed"
        numbers_qs = self.mobile_numbers_set.filter(confirmed_at__isnull=True)
        return [numbers.mobile for numbers in numbers_qs]

    def confirm_mobile(self, confirmation_key, save=True):
        """
        Attempt to confirm an mobile using the given key.
        Returns the mobile that was confirmed, or raise an exception.
        """
        numbers = self.mobile_numbers_set.confirm(confirmation_key, save=save)
        return numbers.mobile

    def add_confirmed_mobile(self, mobile):
        "Adds an mobile to the user that's already in the confirmed state"
        # if mobile already exists, let exception be thrown
        numbers = self.mobile_numbers_set.create_confirmed(mobile)
        return numbers.key

    def add_unconfirmed_mobile(self, mobile):
        "Adds an unconfirmed mobile number and returns it's confirmation key"
        # if mobile already exists, let exception be thrown
        numbers = self.mobile_numbers_set.create_unconfirmed(mobile)
        return numbers.key

    def add_mobile_if_not_exists(self, mobile):
        """
        If the user already has the mobile, and it's confirmed, do nothing
        and return None.

        If the user already has the mobile, and it's unconfirmed, reset the
        confirmation. If the confirmation is unexpired, do nothing. Return
        the confirmation key of the mobile.
        """
        try:
            numbers = self.mobile_numbers_set.get(mobile=mobile)
        except MobileNumbers.DoesNotExist:
            key = self.add_unconfirmed_mobile(mobile)
        else:
            if not numbers.is_confirmed:
                key = numbers.reset_confirmation()
            else:
                key = None

        return key

    def reset_mobile_confirmation(self, mobile):
        "Reset the expiration of an mobile confirmation"
        numbers = self.mobile_numbers_set.get(mobile=mobile)
        return numbers.reset_confirmation()

    def remove_mobile(self, mobile):
        "Remove an mobile address"
        # if mobile already exists, let exception be thrown
        if mobile == self.get_primary_mobile():
            raise MobileIsPrimary()
        numbers = self.mobile_numbers_set.get(mobile=mobile)
        numbers.delete()


class MobileNumbersManager(models.Manager):

    def generate_key(self):
        "Generate a new random key and return it"
        # sticking with the django defaults
        code = ''.join(random.choice(string.digits) for i in range(6))
        return code

    def create_confirmed(self, mobile, user=None):
        "Create an mobile numbers in the confirmed state"
        user = user or getattr(self, 'instance', None)
        if not user:
            raise ValueError('Must specify user or call from related manager')
        key = self.generate_key()
        now = timezone.now()
        # let mobile-already-exists exception propogate through
        numbers = self.create(
            user=user, mobile=mobile, key=key, set_at=now, confirmed_at=now,
        )
        return numbers

    def create_unconfirmed(self, mobile, user=None):
        "Create an mobile numbers in the unconfirmed state"
        user = user or getattr(self, 'instance', None)
        if not user:
            raise ValueError('Must specify user or call from related manager')
        key = self.generate_key()
        # let email-already-exists exception propogate through
        numbers = self.create(user=user, mobile=mobile, key=key)
        unconfirmed_mobile_created.send(sender=user, mobile=mobile)
        return numbers

    def confirm(self, key, user=None, save=True):
        "Confirm an mobile number. Returns the numbers that was confirmed."
        queryset = self.all()
        if user:
            queryset = queryset.filter(user=user)
        numbers = queryset.get(key=key)

        if numbers.is_key_expired:
            raise MobileConfirmationExpired()

        if not numbers.is_confirmed:
            numbers.confirmed_at = timezone.now()
            if save:
                numbers.save(update_fields=['confirmed_at'])
                email_confirmed.send(sender=numbers.user, email=numbers.email)

        return numbers


class MobileNumbers(models.Model):
    "An mobile number belonging to a User"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='mobile_numbers_set',
    )
    mobile = PhoneNumberField(null=False,default='+201000000000')
    key = models.CharField(max_length=40, unique=True)

    set_at = models.DateTimeField(
        default=timezone.now,
        help_text=_('When the confirmation key expiration was set'),
    )
    confirmed_at = models.DateTimeField(
        blank=True, null=True,
        help_text=_('First time this mobile was confirmed'),
    )
    sid= models.CharField(max_length=64, blank=True, null=True)
    
    objects = MobileNumbersManager()

    class Meta:
        unique_together = (('user', 'mobile'),)
        verbose_name_plural = "mobile numbers"

    def __unicode__(self):
        return '{} <{}>'.format(self.user, self.mobile)

    @property
    def is_confirmed(self):
        return self.confirmed_at is not None

    @property
    def is_primary(self):
        return bool(self.user.mobile == self.mobile)

    @property
    def key_expires_at(self):
        # By default, keys don't expire. If you want them to, set
        # settings.SIMPLE_EMAIL_CONFIRMATION_PERIOD to a timedelta.
        period = getattr(
            settings, 'SIMPLE_EMAIL_CONFIRMATION_PERIOD', None
        )
        return self.set_at + period if period is not None else None

    @property
    def is_key_expired(self):
        return self.key_expires_at and timezone.now() >= self.key_expires_at

    def reset_confirmation(self):
        """
        Re-generate the confirmation key and key expiration associated
        with this mobile.  Note that the previou confirmation key will
        cease to work.
        """
        self.key = self._default_manager.generate_key()
        self.set_at = timezone.now()

        self.confirmed_at = None
        self.save(update_fields=['key', 'set_at', 'confirmed_at'])
        return self.key


# by default, auto-add unconfirmed MobileNumbers objects for new Users
if getattr(settings, 'SIMPLE_EMAIL_CONFIRMATION_AUTO_ADD', True):
    def auto_add(sender, **kwargs):
        if sender == get_user_model() and kwargs['created']:
            user = kwargs.get('instance')
            # softly failing on using these methods on `user` to support
            # not using the SimpleEmailConfirmationMixin in your User model
            # https://github.com/mfogel/django-simple-email-confirmation/pull/3
            if hasattr(user, 'get_primary_mobile'):
                mobile = user.get_primary_mobile()
            else:
                mobile = user.mobile
            if hasattr(user, 'add_unconfirmed_mobile'):
                user.add_unconfirmed_mobile(mobile)
            else:
                user.mobile_numbers_set.create_unconfirmed(mobile)

    # TODO: try to only connect this to the User model. We can't use
    #       get_user_model() here - results in import loop.

    post_save.connect(auto_add)
