from rest_framework import mixins, permissions, viewsets

from apps.cards.models import Card, Rule

from ...mixins import DestroyModelMixin
from .serializers import CardSerializer, TransferSerializer, RuleSerializer, VisaStrategy


class CardsViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   DestroyModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = CardSerializer
    queryset = Card.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(family=self.request.user.parent.family)
        return queryset


class RulesViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(card__family=self.request.user.parent.family)

    def perform_delete(self, instance):
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
                        'controlType': rule.merchant_type,
                        'isControlEnabled': True,
                        'shouldDeclineAll': True,
                        'shouldAlertOnDecline': True
                    }
                ]
            }
        visa_strategy.delete_rule(rule.card.visa_document_id, **params)


class TransfersViewSet(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]
