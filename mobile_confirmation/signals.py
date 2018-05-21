from django.dispatch import Signal

mobile_confirmed = Signal(providing_args=['user', 'mobile'])
unconfirmed_mobile_created = Signal(providing_args=['user', 'mobile'])
primary_mobile_changed = Signal(
    providing_args=['user', 'new_mobile', 'old_mobile'],
)

