import os
import unittest
from unit import Unit
from unit.models.account_end_of_day import *


class AccountEndOfDayE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_list_account_end_of_day(self):
        params = AccountEndOfDayListParams(10, 0, customer_id="49430")
        response = self.client.account_end_of_day.list(params)
        for a in response.data:
            self.assertTrue(a.type == "accountEndOfDay")


if __name__ == '__main__':
    unittest.main()

