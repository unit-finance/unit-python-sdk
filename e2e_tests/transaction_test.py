import os
import unittest
from unit import Unit
from unit.models.transaction import PatchTransactionRequest, ListTransactionParams, WireTransactionDTO

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def test_list_and_get_transactions():
    transaction_ids = []
    response = client.transactions.list()

    for t in response.data:
        assert "Transaction" in t.type
        transaction_ids.append(t.id)

    for id in transaction_ids:
        response = client.transactions.get(id)
        assert "Transaction" in response.data.type

def test_update_transaction():
    response = client.transactions.list()
    tags = {"purpose": "test"}

    for t in response.data:
        account_id = t.relationships["account"].id
        transaction_id = t.id
        request = PatchTransactionRequest(account_id, transaction_id, tags)
        response = client.transactions.update(request)
        assert "Transaction" in t.type

def test_sending_wire_transaction():
    wire_transaction_api_response = {
        "type": "wireTransaction",
        "id": "111111",
        "attributes": {
            "createdAt": "2022-02-10T17:56:49.235Z",
            "amount": 200,
            "direction": "Debit",
            "balance": 435055,
            "summary": "Wire to April Oniel | Wire payment",
            "counterparty": {
                "name": "April Oniel",
                "routingNumber": "812345678",
                "accountNumber": "1000000001",
                "accountType": "Checking",
                "bankName": "Bank Name"
            },
            "description": "Wire payment",
            "referenceForBeneficiary": "Test"
        },
        "relationships": {
            "account": {
                "data": {
                    "type": "account",
                    "id": "1"
                }
            },
            "customer": {
                "data": {
                    "type": "customer",
                    "id": "1"
                }
            },
            "customers": {
                "data": [
                    {
                        "type": "customer",
                        "id": "1"
                    }
                ]
            },
            "org": {
                "data": {
                    "type": "org",
                    "id": "1"
                }
            }
        }
    }
    id = wire_transaction_api_response["id"]
    attributes = wire_transaction_api_response["attributes"]
    relationships = wire_transaction_api_response["relationships"]
    _type = wire_transaction_api_response["type"]

    transaction = WireTransactionDTO.from_json_api(id, _type, attributes, relationships)

    assert transaction.id == id
    assert transaction.attributes["counterparty"].routing_number == "812345678"
    assert transaction.attributes["referenceForBeneficiary"] == "Test"


def test_receiving_wire_transaction():
    wire_transaction_api_response = {
        "type": "wireTransaction",
        "id": "111111",
        "attributes": {
            "createdAt": "2022-02-10T17:56:49.235Z",
            "amount": 200,
            "direction": "Debit",
            "balance": 435055,
            "summary": "Wire to April Oniel | Wire payment",
            "counterparty": {
                "name": "April Oniel",
                "routingNumber": "812345678",
                "accountNumber": "1000000001",
                "accountType": "Checking",
                "bankName": "Bank Name"
            },
            "description": "Wire payment",
            "senderReference": "Test"
        },
        "relationships": {
            "account": {
                "data": {
                    "type": "account",
                    "id": "1"
                }
            },
            "customer": {
                "data": {
                    "type": "customer",
                    "id": "1"
                }
            },
            "customers": {
                "data": [
                    {
                        "type": "customer",
                        "id": "1"
                    }
                ]
            },
            "org": {
                "data": {
                    "type": "org",
                    "id": "1"
                }
            }
        }
    }

    id = wire_transaction_api_response["id"]
    attributes = wire_transaction_api_response["attributes"]
    relationships = wire_transaction_api_response["relationships"]
    _type = wire_transaction_api_response["type"]

    transaction = WireTransactionDTO.from_json_api(id, _type, attributes, relationships)

    assert transaction.id == id
    assert transaction.attributes["counterparty"].routing_number == "812345678"
    assert transaction.attributes["senderReference"] == "Test"

def test_list_and_get_transactions_with_type():
    transaction_ids = []
    response = client.transactions.list(ListTransactionParams(100, 0, type=["Fee", "ReceivedAch"]))

    for t in response.data:
        assert t.type == "receivedAchTransaction" or t.type == "feeTransaction"
        transaction_ids.append(t.id)

    for id in transaction_ids:
        response = client.transactions.get(id)
        assert response.data.type == "receivedAchTransaction" or response.data.type == "feeTransaction"
