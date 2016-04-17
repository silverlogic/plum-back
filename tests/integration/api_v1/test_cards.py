import pytest

import tests.factories as f
import tests.helpers as h
from tests.mixins import ApiMixin

pytestmark = pytest.mark.django_db


class TestCardCreate(ApiMixin):
    view_name = 'cards-list'

    @pytest.fixture
    def data(self, parent_client):
        return {
            'owner_type': 'parent',
            'owner_id': parent_client.user.parent.pk,
            'name_on_card': 'John Wilks',
            'number': '4856200001123821',
            'expiration_date': '2018-06-04',
        }

    @pytest.fixture
    def kid_data(self, parent_client):
        self.kid = f.KidFactory(family=parent_client.user.parent.family)
        return {
            'owner_type': 'kid',
            'owner_id': self.kid.pk,
            'name_on_card': 'John Wilks',
            'number': '4856200001123821',
            'expiration_date': '2018-06-04',
        }

    def test_guest_cant_create(self, client, data):
        r = client.post(self.reverse(), data)
        h.responseUnauthorized(r)

    def test_parent_can_create_for_themselves(self, parent_client, data):
        r = parent_client.post(self.reverse(), data)
        h.responseCreated(r)

    def test_parent_can_create_for_their_kid(self, parent_client, kid_data):
        r = parent_client.post(self.reverse(), kid_data)
        h.responseCreated(r)
