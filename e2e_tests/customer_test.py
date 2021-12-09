import os
import unittest
from unit import Unit
from unit.models.customer import *


class CustomerE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def get_customer_by_type(self, type: str):
        response = self.client.customers.list()
        for c in response.data:
            if c.type == type:
                return c
        return None

    def test_update_individual_customer(self):
        individual_customer_id = self.get_customer_by_type("individualCustomer").id
        request = PatchIndividualCustomerRequest(individual_customer_id, phone=Phone("1", "1115551111"))
        response = self.client.customers.update(request)
        self.assertTrue(response.data.type == "individualCustomer")

    def test_update_business_customer(self):
        business_customer_id = self.get_customer_by_type("businessCustomer").id
        request = PatchBusinessCustomerRequest(business_customer_id, phone=Phone("1", "1115551111"))
        response = self.client.customers.update(request)
        self.assertTrue(response.data.type == "businessCustomer")

    def test_get_customer(self):
        customer_ids = []
        response = self.client.customers.list()
        for c in response.data:
            customer_ids.append(c.id)

        for id in customer_ids:
            response = self.client.customers.get(id)
            self.assertTrue(response.data.type == "individualCustomer" or response.data.type == "businessCustomer")

    def test_list_customers(self):
        response = self.client.customers.list()
        for customer in response.data:
            self.assertTrue(customer.type == "individualCustomer" or customer.type == "businessCustomer")


if __name__ == '__main__':
    unittest.main()
