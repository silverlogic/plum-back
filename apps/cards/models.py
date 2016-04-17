from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
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

    visa_document_id = models.CharField(max_length=255, blank=True)


class Rule(models.Model):
    Type = Choices(
        ('global', 'global_', _('Global')),
        ('merchant', 'merchant', _('Merchant'))
    )
    MerchantType = Choices(
        ('MCT_ADULT_ENTERTAINMENT', 'adult_entertainment', 'Adult Entertainment'),
        ('MCT_AIRFARE', 'airfare', 'Airfare'),
        ('MCT_ALCOHOL', 'alcohol', 'Alcohol'),
        ('MCT_APPAREL_AND_ACCESSORIES', 'apparel', 'Apparel and Accesories'),
        ('MCT_AUTOMOTIVE', 'auto', 'Automotive'),
        ('MCT_CAR_RENTAL', 'car_rental', 'Car Rental'),
        ('MCT_ELECTRONICS', 'electronics', 'Electronics'),
        ('MCT_ENTERTAINMENT_AND_SPORTINGEVENTS', 'entertainment', 'Entertainment and Sporting Events'),
        ('MCT_GAMBLING', 'gambling', 'Gambling'),
        ('MCT_GAS_AND_PETROLEUM', 'gas', 'Gas and Petroleum'),
        ('MCT_GROCERY', 'grocery', 'Grocery'),
        ('MCT_HOTEL_AND_LODGING', 'hotel_and_lodging', 'Hotel and Lodging'),
        ('MCT_HOUSEHOLD', 'household', 'Household'),
        ('MCT_PERSONAL_CARE', 'personal_care', 'Personal Care'),
        ('MCT_RECREATION', 'recreation', 'Recreation'),
        ('MCT_SMOKE_AND_TOBACCO' 'smoke_and_tobacco', 'Smoke and Tobacco'),
    )

    card = models.ForeignKey('Card')
    type = models.CharField(max_length=100, choices=Type)
    merchant_types = ArrayField(models.CharField(max_length=255, choices=MerchantType), blank=True, default=list)


class Transfer(models.Model):
    from_card = models.ForeignKey('Card', related_name='from_transfers')
    to_card = models.ForeignKey('Card', related_name='to_transfers')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
