import os
import unittest
from unit import Unit
from unit.models.transaction import PatchTransactionRequest


class TransactionE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_list_and_get_transactions(self):
        transaction_ids = []
        response = self.client.transactions.list()

        for t in response.data:
            self.assertTrue("Transaction" in t.type)
            transaction_ids.append(t.id)

        for id in transaction_ids:
            response = self.client.transactions.get(id)
            self.assertTrue("Transaction" in response.data.type)

    def test_update_transaction(self):
        response = self.client.transactions.list()
        tags = {"purpose": "test"}

        for t in response.data:
            account_id = t.relationships["account"].id
            transaction_id = t.id
            request = PatchTransactionRequest(account_id, transaction_id, tags)
            response = self.client.transactions.update(request)
            self.assertTrue("Transaction" in t.type)


if __name__ == '__main__':
    unittest.main()
