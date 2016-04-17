import pytest

import tests.factories as f
import tests.helpers as h
from tests.mixins import ApiMixin

pytestmark = pytest.mark.django_db


class TestKidCreate(ApiMixin):
    view_name = 'kids-list'

    @pytest.fixture
    def data(self):
        return {
            'name': 'JOHNNNYYYY'
        }

    def test_parent_can_create(self, parent_client, data):
        r = parent_client.post(self.reverse(), data)
        h.responseCreated(r)


class TestKidCards(ApiMixin):
    view_name = 'kids-cards'

    def test_it(self, parent_client):
        kid = f.KidFactory()
        card = f.CardFactory(owner=kid)
        f.CardFactory()
        r = parent_client.get(self.reverse(kwargs={'pk': kid.pk}))
        h.responseOk(r)
        assert r.data['count'] == 1
        assert r.data['results'][0]['id'] == card.pk
