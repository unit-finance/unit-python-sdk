import os
import unittest
from api.unit import Unit
from models.counterparty import *
from e2e_tests.account_test import AccountE2eTests


class CounterpartyE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def create_counterparty(self):
        AccountTests = AccountE2eTests()
        customer_id = AccountTests.create_individual_customer()
        request = CreateCounterpartyRequest("Joe Doe", "123456789", "123", "Checking", "Person",
                                            {"customer": Relationship("customer", customer_id)})
        return self.client.counterparty.create(request)

    def test_create_counterparty(self):
        response = self.create_counterparty()
        self.assertTrue(response.data.type == "achCounterparty")


if __name__ == '__main__':
    unittest.main()
