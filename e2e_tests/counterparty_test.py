import os
import unittest
from unit import Unit
from unit.models.counterparty import *
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

    def test_delete_counterparty(self):
        counterparty_id = self.create_counterparty().data.id
        response = self.client.counterparty.delete(counterparty_id)
        self.assertTrue(response.data == [])

    def test_get_counterparty(self):
        counterparty_id = self.create_counterparty().data.id
        response = self.client.counterparty.get(counterparty_id)
        self.assertTrue(response.data.type == "achCounterparty")

    def test_counterparty_list(self):
        response = self.client.counterparty.list()
        for c in response.data:
            self.assertTrue(c.type == "achCounterparty")


if __name__ == '__main__':
    unittest.main()
