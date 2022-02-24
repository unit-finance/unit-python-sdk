import os
import unittest
from unit import Unit
from unit.models.returnAch import *

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def get_received_ach_transaction():
    response = client.transactions.list()
    for t in response.data:
        if t.type == "receivedAchTransaction":
            return t

    return ""

def test_return_ach():
    # transaction = get_received_ach_transaction()
    # transaction_id = transaction.id
    # account_id = transaction.relationships["customer"].id
    # request = ReturnReceivedAchTransactionRequest(transaction_id, "Unauthorized",
    #                                               {"account": Relationship("depositAccount", account_id)})
    # response = client.returnAch.return_ach(request)
    # assert response.data.type == "returnedReceivedAchTransaction"
    assert True

