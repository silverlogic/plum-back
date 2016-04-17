from django.contrib.contenttypes.models import ContentType

from rest_framework import decorators, mixins, permissions, viewsets
from rest_framework.response import Response

from apps.cards.models import Card
from apps.family.models import Kid

from ...mixins import DestroyModelMixin
from ..cards.serializers import CardSerializer
from .serializers import KidSerializer


class KidsViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = KidSerializer
    queryset = Kid.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(family=self.request.user.parent.family)
        return queryset

    @decorators.detail_route(methods=['GET'], serializer_class=CardSerializer)
    def cards(self, request, pk=None):
        kid_ct = ContentType.objects.get_for_model(Kid)

        queryset = Card.objects.filter(owner_type=kid_ct, owner_id=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
