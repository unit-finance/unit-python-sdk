import os
import unittest
from unit import Unit
from unit.models.bill_pay import *


class BillPayE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_get_billers(self):
        request = GetBillersRequest("Electric")
        response = self.client.billPays.get(request)
        for b in response.data:
            self.assertTrue(b.type == "biller")

    def test_get_billers_with_page_param(self):
        request = GetBillersRequest("Electric", 1)
        response = self.client.billPays.get(request)
        for b in response.data:
            self.assertTrue(b.type == "biller")


if __name__ == '__main__':
    unittest.main()

