from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from profile.models import Profile
import uuid
# Create your models here.


class FollowManager(models.Manager):
    """
    Manager for Follow model.
    """

    def is_following(self, user, actor,actor_slug):
        """
        Check if a user is following an instance.
        """
        if not user or user.is_anonymous():
            return False
        queryset = Follow.objects.filter(profile=user,actor=actor,actor_slug=actor_slug)
        return queryset.filter(profile=user).exists()

    def followers(self, actor,actor_slug):
        """
        Returns a list of User objects who are following this actor (eg who is following this shop).
        can be used to get the followers of any shop or prodact
        """
        followers = Follow.objects.filter(actor=actor)
        data = []
        for follow in followers:
        	data.append({
        		'id': str(follow.id),
        		'at': str(follow.started),
        		'actor':follow.actor,
        		'actor_slug':follow.actor_slug,
        		'actor_uuid':follow.actor_uuid,
        		})
        return data

    def following(self, user):
        """
        Returns a list of actors that the given user is following (eg who im following).
        can be used to get the list of shops or prodact that the user following them
        """
        actors = Follow.objects.filter(profile=user)
        data = []
        for follow in actors:
        	data.append({
        		'id': str(follow.id),
        		'at': str(follow.started),
        		'actor':follow.actor,
        		'actor_slug':follow.actor_slug,
        		'actor_uuid':follow.actor_uuid,
        		})
        return data

class Follow(models.Model):
    """
    Lets a user follow specific actor
    (actor) maybe shop or profile or prodact 
    """
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile     = models.ForeignKey(Profile,null=True,blank=True)

    actor       = models.ForeignKey(ContentType,db_index=True)
    actor_uuid  = models.UUIDField(primary_key=False, editable=False,default=uuid.uuid4)
    actor_slug  = models.SlugField(max_length=50,blank=True, null=True,default='wawa')
    started     = models.DateTimeField(default=timezone.now, db_index=True)
    objects     = FollowManager()

    class Meta:
    	unique_together = ('profile', 'actor_slug', 'id')

    def __unicode__(self):
		return '%s -> %s' % (self.profile, self.actor_slug)



# convenient accessors
followers    = Follow.objects.followers
following    = Follow.objects.following
is_following = Follow.objects.is_following



