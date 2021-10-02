import os
import unittest
from api.unit import Unit
from e2e_tests.transaction_test import TransactionE2eTests
from models.returnAch import ReturnReceivedAchTransactionRequest

class ReturnAchE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def get_received_ach_transaction(self):
        response = self.client.transactions.list()
        for t in response.data:
            if t.type == "receivedAchTransaction":
                return t.id

        return ""

    def test_return_ach(self):
        transaction_id = get_received_ach_transaction()
        request = ReturnReceivedAchTransactionRequest(transaction_id, "Unauthorized")
        response = self.client.returnAch.return_ach(request)
        self.assertTrue(response.data.type == "returnedReceivedAchTransaction")


if __name__ == '__main__':
    unittest.main()
