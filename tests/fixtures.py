from django.core import mail

import pytest
from rest_framework.test import APIClient

import tests.factories as f


class Client(APIClient):
    def force_authenticate(self, user):
        self.user = user
        super().force_authenticate(user)


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def parent_client():
    client = Client()
    parent = f.ParentFactory()
    client.force_authenticate(parent.user)
    return client


@pytest.fixture
def outbox():
    return mail.outbox
