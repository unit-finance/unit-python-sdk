import os
import unittest
from api.unit import Unit
from models.fee import *
from e2e_tests.account_test import AccountE2eTests


class FeeE2eTests(unittest.TestCase):
    def test_create_individual_application(self):
        token = os.environ.get("token")
        client = Unit("https://api.s.unit.sh", token)

        AccountTests = AccountE2eTests()
        deposit_account_id = AccountTests.create_deposit_account().data.id

        request = CreateFeeRequest(150, "test fee", {"account": Relationship("depositAccount", deposit_account_id)})
        response = client.fees.create(request)
        self.assertTrue(response.data.type == "fee")


if __name__ == '__main__':
    unittest.main()

