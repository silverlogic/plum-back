from decimal import Decimal

from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from apps.family.models import Kid
from apps.cards.models import Card

from ...serializers import ModelSerializer


class KidSerializer(ModelSerializer):
    total_amount_spent = serializers.SerializerMethodField()
    total_amount_on_cards = serializers.SerializerMethodField()

    class Meta:
        model = Kid
        fields = ('id', 'name', 'avatar', 'total_amount_spent', 'total_amount_on_cards',
                  'allowance', 'savings_match',)

    def create(self, validated_data):
        validated_data['family'] = self.context['request'].user.parent.family
        return super().create(validated_data)

    def get_total_amount_spent(self, obj):
        return Card.objects.filter(
            owner_type=ContentType.objects.get_for_model(Kid),
            owner_id=obj.id,
        ).aggregate(total=Sum('amount_spent'))['total'] or Decimal(0)

    def get_total_amount_on_cards(self, obj):
        return Card.objects.filter(
            owner_type=ContentType.objects.get_for_model(Kid),
            owner_id=obj.id,
        ).aggregate(total=Sum('amount_on_card'))['total'] or Decimal(0)
