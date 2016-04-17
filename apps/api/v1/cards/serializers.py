from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from apps.cards.models import Card
from apps.family.models import Kid, Parent


class OwnerTypeField(serializers.Field):
    def to_internal_value(self, data):
        if data == 'parent':
            return ContentType.objects.get_for_model(Parent)
        elif data == 'kid':
            return ContentType.objects.get_for_model(Kid)

    def to_representation(self, obj):
        return obj.model


class CardSerializer(serializers.ModelSerializer):
    owner_type = OwnerTypeField()

    class Meta:
        model = Card
        fields = ('id', 'owner_type', 'owner_id', 'name_on_card',
                  'number', 'expiration_date', 'type', 'sub_type',)
        read_only_fields = ('type', 'sub_type',)

    def create(self, validated_data):
        visa_strategy = VisaStubStrategy()
        result = visa_strategy.general_inquiry(
            primary_account_number=validated_data['number']
        )
        validated_data['family'] = self.context['request'].user.parent.family
        validated_data['type'] = result['cardTypeCode']
        validated_data['sub_type'] = result['cardSubtypeCode']
        return super().create(validated_data)


class VisaStubStrategy:
    def general_inquiry(self, primary_account_number):
        return {
            "status": {
                "statusCode": "CDI000",
                "statusDescription": "Success"
            },
            "cardProductId": "A",
            "cardProductName": "Visa Traditional",
            "cardProductSubtypeCode": "",
            "cardProductSubtypeDescription": "",
            "cardTypeCode": "C",
            "cardSubtypeCode": "",
            "cardPlatformCode": "CN",
            "issuerName": "WELLS FARGO BANK, NATIONAL ASSOCIATION",
            "bin": "446539",
            "countryCode": "840"
        }
