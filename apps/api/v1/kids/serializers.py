from apps.family.models import Kid

from ...serializers import ModelSerializer


class KidSerializer(ModelSerializer):
    class Meta:
        model = Kid
        fields = ('id', 'name', 'avatar',)

    def create(self, validated_data):
        validated_data['family'] = self.context['request'].user.parent.family
        return super().create(validated_data)
