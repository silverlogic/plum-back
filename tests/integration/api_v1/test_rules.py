import pytest

from apps.cards.models import Rule

import tests.factories as f
import tests.helpers as h
from tests.mixins import ApiMixin

pytestmark = pytest.mark.django_db


class TestRuleCreate(ApiMixin):
    view_name = 'rules-list'

    def test_parent_can_create(self, parent_client):
        card = f.CardFactory()
        data = {
            'card': card.pk,
            'type': Rule.Type.global_,
        }
        r = parent_client.post(self.reverse(), data)
        h.responseCreated(r)

    def test_parent_can_create_merchant(self, parent_client):
        card = f.CardFactory()
        data = {
            'card': card.pk,
            'type': Rule.Type.merchant,
            'merchant_types': [
                Rule.MerchantType.household,
                Rule.MerchantType.recreation,
            ]
        }
        r = parent_client.post(self.reverse(), data)
        h.responseCreated(r)
