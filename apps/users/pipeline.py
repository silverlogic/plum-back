import logging
import uuid

from django.core.files.base import ContentFile

import requests
from avatar.models import Avatar

from apps.family.models import Family, Parent, Kid

from .models import User

logger = logging.getLogger(__name__)


def create_user(strategy, backend, details, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    user = User.objects.create(email=details.get('email'))

    if not backend.invite_code:
        family = Family.objects.create()
        Parent.objects.create(family=family, user=user,
                              first_name=details.get('first_name'),
                              last_name=details.get('last_name'))
    else:
        kid = Kid.objects.get(pk=int(backend.invite_code))
        kid.user = user
        kid.save()

    response = kwargs['response']
    url = 'http://graph.facebook.com/%s/picture?type=large' % response['id']
    avatar_file = ContentFile(requests.get(url).content)
    avatar = Avatar(user=user, primary=True)
    file_name = str(uuid.uuid4())
    avatar.avatar.save(file_name, avatar_file)

    return {
        'is_new': True,
        'user': user
    }
