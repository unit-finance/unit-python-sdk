import os
import unittest
from api.unit import Unit
from models.customerToken import *


class CustomerTokenE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_create_token(self):
        request = CreateCustomerToken("101217", "customers accounts")
        response = self.client.customerTokens.create_token(request)
        self.assertTrue(response.data.type == "customerBearerToken")

    def test_create_token_verification(self):
        request = CreateCustomerTokenVerification("101217", "sms")
        response = self.client.customerTokens.create_token_verification(request)
        self.assertTrue(response.data.type == "customerTokenVerification")


if __name__ == '__main__':
    unittest.main()

