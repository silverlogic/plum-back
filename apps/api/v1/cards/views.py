from rest_framework import mixins, permissions, viewsets

from apps.cards.models import Card

from ...mixins import DestroyModelMixin
from .serializers import CardSerializer


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
