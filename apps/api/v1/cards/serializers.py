from django.contrib.contenttypes.models import ContentType

import requests
from rest_framework import serializers

from apps.cards.models import Card, Transfer, Rule, Transaction
from apps.family.models import Kid, Parent

from ...serializers import ModelSerializer


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
                  'number', 'expiration_date', 'type', 'sub_type',
                  'amount_spent', 'amount_on_card',)
        read_only_fields = ('type', 'sub_type', 'amount_spent', 'amount_on_card',)

    def create(self, validated_data):
        visa_strategy = VisaStubStrategy()
        result = visa_strategy.general_inquiry(
            primary_account_number=validated_data['number']
        )
        validated_data['family'] = self.context['request'].user.parent.family
        validated_data['type'] = result['cardTypeCode']
        validated_data['sub_type'] = result['cardSubtypeCode']
        return super().create(validated_data)


class RuleSerializer(ModelSerializer):
    class Meta:
        model = Rule
        fields = ('id', 'card', 'type', 'merchant_types',)

    def create(self, validated_data):
        visa_strategy = VisaStrategy()

        for rule in validated_data['card'].rules.all():
            if rule.type == rule.Type.global_:
                params = {
                    'globalControl': {
                        'isControlEnabled': True,
                        'shouldDeclineAll': True,
                        'shouldAlertOnDecline': True,
                    }
                }
            else:
                params = {
                    'merchantControls': [
                        {
                            'controlType': rule.merchant_type,
                            'isControlEnabled': True,
                            'shouldDeclineAll': True,
                            'shouldAlertOnDecline': True
                        }
                    ]
                }
            visa_strategy.delete_rule(rule.card.visa_document_id, **params)
            rule.delete()

        rule = super().create(validated_data)
        if not rule.card.visa_document_id:
            document_id = visa_strategy.register_card('4224903143151010')
            rule.card.visa_document_id = document_id
            rule.card.save()

        if rule.type == rule.Type.global_:
            params = {
                'globalControl': {
                    'isControlEnabled': True,
                    'shouldDeclineAll': True,
                    'shouldAlertOnDecline': True,
                }
            }
        else:
            params = {
                'merchantControls': [
                    {
                        'controlType': merchant_type,
                        'isControlEnabled': True,
                        'shouldDeclineAll': True,
                        'shouldAlertOnDecline': True
                    } for merchant_type in rule.merchant_types
                ]
            }
        visa_strategy.create_rule(rule.card.visa_document_id, **params)
        return rule

    def update(self, instance, validated_data):
        rule = instance
        visa_strategy = VisaStrategy()
        if rule.type == rule.Type.global_:
            params = {
                'globalControl': {
                    'isControlEnabled': True,
                    'shouldDeclineAll': True,
                    'shouldAlertOnDecline': True,
                }
            }
        else:
            params = {
                'merchantControls': [
                    {
                        'controlType': merchant_type,
                        'isControlEnabled': True,
                        'shouldDeclineAll': True,
                        'shouldAlertOnDecline': True
                    } for merchant_type in rule.merchant_types
                ]
            }
        visa_strategy.delete(rule.card.visa_document_id, **params)

        super().update(instance, validated_data)

        visa_strategy.create_rule(rule.card.visa_document_id, **params)
        return rule


class TransferSerializer(ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('id', 'from_card', 'to_card', 'amount',)

    def create(self, validated_data):
        visa_strategy = VisaStrategy()
        visa_strategy.pull_funds(
            sender_primary_account_number=validated_data['from_card'].number,
            sender_card_expiry_date=validated_data['from_card'].expiration_date.strftime('%Y-%m'),
            amount=str(validated_data['amount'])
        )
        visa_strategy.push_funds()
        return super().create(validated_data)


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'card', 'amount', 'merchant_name', 'status', 'when',)


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


class VisaStrategy:
    headers = {
        'content-type': 'application/json',
        'Accept': 'application/json,application/octet-stream'
    }
    cert = ('/home/ryan/projects/tsl/hackathons/2016-04-16-emerge-americas/cert.pem', '/home/ryan/projects/tsl/hackathons/2016-04-16-emerge-americas/key_Plum.pem')
    auth = ('H6DR41S1COCZSFN8PE6A21_N7hDuLMlLLO07EVFxLVwzHKwCw', 'E0UJZwS241ZxCc8tEYYxGqUMVVnCg6fDo5Yq3')

    def pull_funds(self, sender_primary_account_number, sender_card_expiry_date, amount):
        body = {
            "amount": "100",
            "acquirerCountryCode": "840",
            "acquiringBin": "408999",
            "businessApplicationId": "AA",
            "cardAcceptor": {
                "address": {
                    "country": "USA",
                    "county": "San Mateo",
                    "state": "CA",
                    "zipCode": "94404"
                },
                "idCode": "ABCD1234ABCD123",
                "name": "Acceptor 1",
                "terminalId": "ABCD1234"
            },
            "localTransactionDateTime": "2016-04-16T18:54:38",
            "retrievalReferenceNumber": "330000550000",
            "senderCardExpiryDate": "2020-03",
            "senderCurrencyCode": "USD",
            "senderPrimaryAccountNumber": "4005520000011126",
            "systemsTraceAuditNumber": "451001"
        }
        response = requests.post(
            url='https://sandbox.api.visa.com/visadirect/fundstransfer/v1/pullfundstransactions',
            cert=self.cert,
            auth=self.auth,
            headers=self.headers,
            json=body
        )
        print(response.json())

    def push_funds(self):
        body = {
            "acquirerCountryCode": "840",
            "acquiringBin": "408999",
            "amount": "349",
            "businessApplicationId": "AA",
            "cardAcceptor": {
                "address": {
                    "country": "USA",
                    "county": "San Mateo",
                    "state": "CA",
                    "zipCode": "94404"
                },
                "idCode": "CA-IDCode-77765",
                "name": "Visa Inc. USA-Foster City",
                "terminalId": "TID-9999"
            },
            "localTransactionDateTime": "2016-04-16T21:19:50",
            "merchantCategoryCode": "6012",
            "recipientName": "rohan",
            "recipientPrimaryAccountNumber": "4957030420210454",
            "retrievalReferenceNumber": "412770451018",
            "senderAccountNumber": "495703042020470",
            "senderName": "Mohammed Qasim",
            "systemsTraceAuditNumber": "451018",
            "transactionCurrencyCode": "USD",
        }
        response = requests.post(
            url='https://sandbox.api.visa.com/visadirect/fundstransfer/v1/pushfundstransactions',
            cert=self.cert,
            auth=self.auth,
            headers=self.headers,
            json=body
        )
        print(response.json())

    def register_card(self, primary_account_number):
        body = {
            "primaryAccountNumber": "4224903143151010"
        }
        response = requests.post(
            'https://sandbox.api.visa.com/vctc/customerrules/v1/consumertransactioncontrols',
            cert=self.cert,
            auth=self.auth,
            headers=self.headers,
            json=body
        )
        print(response.json())
        return response.json()['resource']['documentID']

    def create_rule(self, document_id, **params):
        body = params
        response = requests.post(
            'https://sandbox.api.visa.com/vctc/customerrules/v1/consumertransactioncontrols/{0}/rules'.format(document_id),
            cert=self.cert,
            auth=self.auth,
            headers=self.headers,
            json=body
        )
        print(response.json())
        return response.json()

    def delete_rule(self, document_id, **params):
        body = params
        response = requests.delete(
            'https://sandbox.api.visa.com/vctc/customerrules/v1/consumertransactioncontrols/{0}/rules'.format(document_id),
            cert=self.cert,
            auth=self.auth,
            headers=self.headers,
            json=body
        )
        print(response.json())
        return response.json()
