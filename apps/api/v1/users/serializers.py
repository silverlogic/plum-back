from django.utils.translation import ugettext_lazy as _

from avatar.templatetags.avatar_tags import avatar_url
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from apps.api.serializers import ModelSerializer
from apps.family.models import Parent
from apps.users.models import User

from ..kids.serializers import KidSerializer


class AvatarSerializer(serializers.Serializer):
    image = Base64ImageField(required=False, allow_null=True, write_only=True)

    def to_representation(self, instance):
        user = instance
        return {
            'full_size': avatar_url(user, 64),
        }


class ParentSerializer(ModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = Parent
        fields = ('id', 'first_name', 'last_name', 'avatar')


class UserSerializer(ModelSerializer):
    parent = ParentSerializer()
    kid = KidSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'parent', 'kid')


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_current_password(self, current_password):
        user = self.context['request'].user
        if not user.check_password(current_password):
            raise serializers.ValidationError(_('That is not your current password.'))
        return current_password

    def save(self):
        user = self.context['request'].user
        user.set_password(self.data['new_password'])
        user.save()
