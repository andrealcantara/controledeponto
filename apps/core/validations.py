from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidationOnlyDay:
    month = 0
    def __init__(self, month=None):
        if month is not None:
            self.month = month

    def __call__(self, value):
        if value < 0 or value > 31 or (self.month == 2 and value > 29):
            raise ValidationError(
                _('%(value)s is not a number day valid.'),
                params={'value': value},
            )
