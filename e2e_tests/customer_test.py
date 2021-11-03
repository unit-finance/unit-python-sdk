import os
import unittest
from unit import Unit
from unit.models.customer import *


class CustomerE2eTests(unittest.TestCase):
    def test_update_individual_customer(self):
        token = os.environ.get("token")
        request = PatchIndividualCustomerRequest("49423", phone=Phone("1", "1115551111"))
        client = Unit("https://api.s.unit.sh", token)
        response = client.customers.update(request)
        self.assertTrue(response.data.type == "individualCustomer")

    def test_update_business_customer(self):
        token = os.environ.get("token")
        request = PatchBusinessCustomerRequest("49430", phone=Phone("1", "1115551111"))
        client = Unit("https://api.s.unit.sh", token)
        response = client.customers.update(request)
        self.assertTrue(response.data.type == "businessCustomer")

    def test_get_customer(self):
        token = os.environ.get("token")
        client = Unit("https://api.s.unit.sh", token)
        response = client.customers.get(49430)
        self.assertTrue(response.data.type == "individualCustomer" or response.data.type == "businessCustomer")

    def test_list_customers(self):
        token = os.environ.get("token")
        client = Unit("https://api.s.unit.sh", token)
        response = client.customers.list()
        for customer in response.data:
            self.assertTrue(customer.type == "individualCustomer" or customer.type == "businessCustomer")


if __name__ == '__main__':
    unittest.main()
