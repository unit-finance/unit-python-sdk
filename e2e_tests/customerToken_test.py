import os
import unittest
from unit import Unit
from e2e_tests.account_test import AccountE2eTests
from unit.models.customerToken import CreateCustomerToken, CreateCustomerTokenVerification


class CustomerTokenE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)
    accountTests = AccountE2eTests()

    def test_create_token(self):
        account_id = self.accountTests.create_individual_customer()
        request = CreateCustomerToken(account_id, "customers accounts")
        response = self.client.customerTokens.create_token(request)
        self.assertTrue(response.data.type == "customerBearerToken")

    def test_create_token_verification(self):
        account_id = self.accountTests.create_individual_customer()
        request = CreateCustomerTokenVerification(account_id, "sms")
        response = self.client.customerTokens.create_token_verification(request)
        self.assertTrue(response.data.type == "customerTokenVerification")


if __name__ == '__main__':
    unittest.main()

