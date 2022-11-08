import os
import unittest

from e2e_tests.helpers.helpers import create_deposit_account
from unit import Unit
from unit.models.fee import *

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def test_create_fee():
    deposit_account_id = create_deposit_account(client).data.id

    request = CreateFeeRequest(150, "test fee", {"account": Relationship("depositAccount", deposit_account_id)})
    response = client.fees.create(request)
    assert response.data.type == "fee"


