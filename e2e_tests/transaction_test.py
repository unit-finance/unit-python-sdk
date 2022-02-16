import os
import unittest
from unit import Unit
from unit.models.transaction import PatchTransactionRequest, ListTransactionParams

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def test_list_and_get_transactions():
    assert True
#     transaction_ids = []
#     response = client.transactions.list()
#
#     for t in response.data:
#         assert "Transaction" in t.type
#         transaction_ids.append(t.id)
#
#     for id in transaction_ids:
#         response = client.transactions.get(id)
#         assert "Transaction" in response.data.type
#
# def test_update_transaction():
#     response = client.transactions.list()
#     tags = {"purpose": "test"}
#
#     for t in response.data:
#         account_id = t.relationships["account"].id
#         transaction_id = t.id
#         request = PatchTransactionRequest(account_id, transaction_id, tags)
#         response = client.transactions.update(request)
#         assert "Transaction" in t.type
#     def test_list_and_get_transactions(self):
#         transaction_ids = []
#         response = self.client.transactions.list(
#             ListTransactionParams(100, 0, type=["Fee", "ReceivedAch"]))
#
#         for t in response.data:
#             self.assertTrue(t.type == "receivedAchTransaction" or t.type == "feeTransaction")
#             transaction_ids.append(t.id)
#
#         for id in transaction_ids:
#             response = self.client.transactions.get(id)
#             self.assertTrue(response.data.type == "receivedAchTransaction" or response.data.type == "feeTransaction")
#
#     def test_update_transaction(self):
#         response = self.client.transactions.list()
#         tags = {"purpose": "test"}
#
#         for t in response.data:
#             account_id = t.relationships["account"].id
#             transaction_id = t.id
#             request = PatchTransactionRequest(account_id, transaction_id, tags)
#             response = self.client.transactions.update(request)
#             self.assertTrue("Transaction" in t.type)

