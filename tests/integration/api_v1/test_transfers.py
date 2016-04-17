import pytest

import tests.factories as f
import tests.helpers as h
from tests.mixins import ApiMixin

pytestmark = pytest.mark.django_db


class TestKidCreate(ApiMixin):
    view_name = 'transfers-list'

    @pytest.fixture
    def data(self):
        return {
            'from_card': f.CardFactory().pk,
            'to_card': f.CardFactory().pk,
            'amount': '100'
        }

    def test_parent_can_create(self, parent_client, data):
        r = parent_client.post(self.reverse(), data)
        h.responseCreated(r)
