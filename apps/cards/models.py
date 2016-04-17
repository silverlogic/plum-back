from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.choices import Choices


class Card(models.Model):
    Type = Choices(
        ('C', 'credit', _('Credit')),
        ('P', 'prepaid', _('Prepaid')),
        ('D', 'debit', _('Prepaid')),
        ('R', 'deferred_debt', _('Deferred Debt')),
        ('H', 'charge', _('Charge Card')),
    )
    SubType = Choices(
        ('N', 'non_reloadable', _('Non-Reloadable')),
        ('R', 'reloadable', _('Reloadable')),
    )

    family = models.ForeignKey('family.Family', related_name='cards')

    owner_type = models.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField()
    owner = GenericForeignKey('owner_type', 'owner_id')

    name_on_card = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    expiration_date = models.DateField(help_text='Day is ignored.')
    type = models.CharField(max_length=100, choices=Type)
    sub_type = models.CharField(max_length=100, choices=SubType)
