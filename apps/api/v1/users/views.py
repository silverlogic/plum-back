from django.contrib.contenttypes.models import ContentType

from rest_framework import decorators, permissions, response, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.cards.models import Card
from apps.family.models import Parent, Kid

from ..cards.serializers import CardSerializer
from .serializers import ChangePasswordSerializer, UserSerializer


class UsersViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer

    @list_route(methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return response.Response(serializer.data)

    @decorators.detail_route(methods=['GET'], permission_classes=[permissions.IsAuthenticated], serializer_class=CardSerializer)
    def me_cards(self, request, pk=None):
        if hasattr(request.user, 'parent'):
            parent_ct = ContentType.objects.get_for_model(Parent)
            queryset = Card.objects.filter(owner_type=parent_ct, owner_id=pk)
        else:
            kid_ct = ContentType.objects.get_for_model(Kid)
            queryset = Card.objects.filter(owner_type=kid_ct, owner_id=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({'detail': 'success'})
