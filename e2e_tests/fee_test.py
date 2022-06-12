import os
import unittest
from unit import Unit
from unit.models.fee import *
from e2e_tests.account_test import create_deposit_account

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def test_create_individual_application():
    deposit_account_id = create_deposit_account().data.id

    request = CreateFeeRequest(150, "test fee", {"account": Relationship("depositAccount", deposit_account_id)})
    response = client.fees.create(request)
    assert response.data.type == "fee"


