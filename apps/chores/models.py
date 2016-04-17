from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices


class Chore(models.Model):
    Status = Choices(
        ('complete', _('Complete')),
        ('incomplete', _('Incomplete')),
    )

    kid = models.ForeignKey('family.Kid')
    name = models.CharField(max_length=100)
    points = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=100, choices=Status, default=Status.incomplete)
