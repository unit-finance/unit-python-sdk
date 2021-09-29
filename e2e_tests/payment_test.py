import os
import unittest
from datetime import datetime, date, timedelta
from api.unit import Unit


class PaymentE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_list_and_get_payments(self):
        payments_ids = []
        response = self.client.payments.list()

        for t in response.data:
            self.assertTrue("Payment" in t.type)
            payments_ids.append(t.id)

        for id in payments_ids:
            response = self.client.payments.get(id)
            self.assertTrue("Payment" in response.data.type)


if __name__ == '__main__':
    unittest.main()
