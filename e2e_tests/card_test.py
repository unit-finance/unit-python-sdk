import os
import unittest
from api.unit import Unit

class MyTestCase(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)
    card_types = ["individualDebitCard", "businessDebitCard", "individualVirtualDebitCard", "businessVirtualDebitCard"]

    def test_get_debit_card(self):
        response = self.client.cards.get("26070")
        self.assertTrue(response.data.type in self.card_types)


if __name__ == '__main__':
    unittest.main()
