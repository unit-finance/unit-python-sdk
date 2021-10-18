import os
import unittest
from api.unit import Unit
from models.returnAch import *


class ReturnAchE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def get_received_ach_transaction(self):
        response = self.client.transactions.list()
        for t in response.data:
            if t.type == "receivedAchTransaction":
                return t

        return ""

    def test_return_ach(self):
        transaction = self.get_received_ach_transaction()
        transaction_id = transaction.id
        account_id = transaction.relationships["account"].id
        request = ReturnReceivedAchTransactionRequest(transaction_id, "Unauthorized",
                                                      {"account": Relationship("depositAccount", account_id)})
        response = self.client.returnAch.return_ach(request)
        self.assertTrue(response.data.type == "returnedReceivedAchTransaction")


if __name__ == '__main__':
    unittest.main()
