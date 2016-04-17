from ...serializers import ModelSerializer

from apps.chores.models import Chore


class ChoreSerializer(ModelSerializer):
    class Meta:
        model = Chore
        fields = ('id', 'kid', 'name', 'points', 'status')
