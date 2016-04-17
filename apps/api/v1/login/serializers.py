import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from requests.exceptions import HTTPError
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from social.apps.django_app.utils import load_backend, load_strategy
from social.exceptions import SocialAuthBaseException

from apps.users.models import User

logger = logging.getLogger(__name__)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, email):
        try:
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('Email does not exist.'))
        return email

    def validate(self, data):
        if not self.user.check_password(data['password']):
            raise serializers.ValidationError({'password': _('Incorrect password.')})
        return data

    def create(self, validated_data):
        return Token.objects.get_or_create(user=self.user)[0]


class FacebookLoginSerializer(serializers.Serializer):
    token = serializers.CharField()

    def create(self, validated_data):
        backend = 'facebook'
        redirect_uri = reverse('social:complete', args=(backend,))
        social_strategy = load_strategy(self.context['request'])
        backend = load_backend(social_strategy, backend, redirect_uri)

        try:
            user = backend.do_auth(validated_data['token'])
        except SocialAuthBaseException as ex:
            raise serializers.ValidationError({'non_field_errors': str(ex)})
        except HTTPError as ex:
            logger.info('Invalid access token: %s', ex.response.json())
            raise serializers.ValidationError({'access_token': 'Invalid access token'})

        if user:
            return Token.objects.get_or_create(user=user)[0]
        else:
            logger.info('Unkown reason for social auth failure')
            raise serializers.ValidationError({'non_field_errors': ['Something went wrong.']})
