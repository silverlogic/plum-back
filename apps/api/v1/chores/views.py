from rest_framework import mixins, permissions, viewsets, filters

from apps.chores.models import Chore

from ...mixins import DestroyModelMixin
from .serializers import ChoreSerializer


class ChoreFilter(filters.FilterSet):
    class Meta:
        model = Chore
        fields = ('kid', 'status',)


class ChoresViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChoreSerializer
    queryset = Chore.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'parent'):
            queryset = queryset.filter(kid__family=self.request.user.parent.family)
        else:
            queryset = queryset.filter(kid__family=self.request.user.kid.family)
        return queryset
