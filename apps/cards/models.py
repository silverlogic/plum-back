from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.choices import Choices
from model_utils.models import TimeStampedModel


class Card(TimeStampedModel):
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

    amount_on_card = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    amount_spent = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    visa_document_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '{} {}'.format(self.name_on_card, self.number[-4:])

    class Meta:
        ordering = ['created']


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

    card = models.ForeignKey('Card', related_name='rules')
    type = models.CharField(max_length=100, choices=Type)
    merchant_types = ArrayField(models.CharField(max_length=255, choices=MerchantType), blank=True, default=list)


class Transfer(models.Model):
    from_card = models.ForeignKey('Card', related_name='from_transfers')
    to_card = models.ForeignKey('Card', related_name='to_transfers')
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return '{} to {}: ${}'.format(self.from_card.number[-4:], self.to_card.number[-4:], self.amount)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.to_card.amount_on_card += self.amount
            self.to_card.save()
        super().save(*args, **kwargs)


class Transaction(models.Model):
    Status = Choices(
        ('approved', _('Approved')),
        ('declined', _('Declined')),
    )

    card = models.ForeignKey('Card')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    merchant_name = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=Status)
    when = models.DateTimeField()

    def __str__(self):
        return '${} at {} as {}'.format(self.amount, self.merchant_name, self.card.number[-4:])

    def save(self, *args, **kwargs):
        if not self.pk:
            self.card.amount_spent += self.amount
            self.card.amount_on_card -= self.amount
            self.card.save()
            self.send_email()
        super().save(*args, **kwargs)

    def send_email(self):
        context = {
            'last_4': self.card.number[-4:],
            'transaction': self
        }
        message = render_to_string('transaction-alert.txt', context=context)
        send_mail('New Transaction', message=message, from_email=None, recipient_list=[parent.user.email for parent in self.card.family.parents.all()])
