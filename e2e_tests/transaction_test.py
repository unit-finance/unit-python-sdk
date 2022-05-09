import os
import unittest
from unit import Unit
from unit.models.transaction import *
from unit.models.codecs import mappings

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

def test_card_transaction():
    card_transaction_api_response = {
          "type": "cardTransaction",
          "id": "410",
          "attributes": {
            "createdAt": "2020-09-20T12:41:43.360Z",
            "direction": "Debit",
            "amount": 10,
            "balance": 89480,
            "summary": "Card transaction details",
            "cardLast4Digits": "2282",
            "merchant": {
              "name": "Europcar Mobility Group",
              "type": 3381,
              "category": "EUROP CAR",
              "location": "Cupertino, CA"
            },
            "recurring": False,
            "interchange": 2.43,
            "paymentMethod": "Contactless",
            "digitalWallet": "Apple",
            "cardVerificationData": {
              "verificationMethod": "CVV2"
            },
            "cardNetwork": "Visa"
          },
          "relationships": {
            "account": {
              "data": {
                "type": "account",
                "id": "10001"
              }
            },
            "customer": {
              "data": {
                "type": "customer",
                "id": "1001"
              }
            }
          }
        }
    id = card_transaction_api_response["id"]
    attributes = card_transaction_api_response["attributes"]
    relationships = card_transaction_api_response["relationships"]
    _type = card_transaction_api_response["type"]

    transaction = CardTransactionDTO.from_json_api(id, _type, attributes, relationships)

    assert transaction.id == id
    assert transaction.attributes["interchange"] == 2.43
    assert transaction.attributes["recurring"] is False
    assert transaction.attributes["paymentMethod"] == "Contactless"
    assert transaction.attributes["cardNetwork"] == "Visa"
    assert transaction.attributes["digitalWallet"] == "Apple"
    assert transaction.attributes["cardVerificationData"]["verificationMethod"] == "CVV2"

def test_atm_transaction():
    atm_transaction_api_response = {
          "type": "atmTransaction",
          "id": "1432",
          "attributes": {
            "createdAt": "2020-07-05T15:49:36.864Z",
            "direction": "Credit",
            "amount": 10000,
            "balance": 12000,
            "summary": "ATM deposit",
            "cardLast4Digits": "2282",
            "atmName": "First National Bank",
            "atmLocation": "Masontown, PA 15461",
            "surcharge": 10,
            "interchange": 15.2,
            "cardNetwork": "Allpoint"
          },
          "relationships": {
            "account": {
              "data": {
                "type": "depositAccount",
                "id": "1000"
              }
            },
            "customer": {
              "data": {
                "type": "customer",
                "id": "3"
              }
            },
            "card": {
              "data": {
                "type": "card",
                "id": "11"
              }
            }
          }
        }

    id = atm_transaction_api_response["id"]
    attributes = atm_transaction_api_response["attributes"]
    relationships = atm_transaction_api_response["relationships"]
    _type = atm_transaction_api_response["type"]

    transaction = AtmTransactionDTO.from_json_api(id, _type, attributes, relationships)

    assert transaction.id == id
    assert transaction.attributes["surcharge"] == 10
    assert transaction.attributes["interchange"] == 15.2
    assert transaction.attributes["cardNetwork"] == "Allpoint"

def test_purchase_transaction():
    purchase_transaction_api_response = {
          "type": "purchaseTransaction",
          "id": "51",
          "attributes": {
            "createdAt": "2020-09-08T12:41:43.360Z",
            "direction": "Debit",
            "amount": 2500,
            "balance": 10523,
            "summary": "Car rental",
            "cardLast4Digits": "2282",
            "merchant": {
              "name": "Europcar Mobility Group",
              "type": 3381,
              "category": "EUROP CAR",
              "location": "Cupertino, CA"
            },
            "coordinates": {
              "longitude": -77.0364,
              "latitude": 38.8951
            },
            "recurring": False,
            "interchange": 2.43,
            "ecommerce": False,
            "cardPresent": True,
            "paymentMethod": "Contactless",
            "digitalWallet": "Apple",
            "cardVerificationData": {
              "verificationMethod": "CVV2"
            },
            "cardNetwork": "Visa"
          },
          "relationships": {
            "account": {
              "data": {
                "type": "account",
                "id": "10001"
              }
            },
            "customer": {
              "data": {
                "type": "customer",
                "id": "3"
              }
            },
            "card": {
              "data": {
                "type": "card",
                "id": "11"
              }
            },
            "authorization": {
              "data": {
                "type": "authorization",
                "id": "40"
              }
            }
          }
        }

    id = purchase_transaction_api_response["id"]
    attributes = purchase_transaction_api_response["attributes"]
    relationships = purchase_transaction_api_response["relationships"]
    _type = purchase_transaction_api_response["type"]

    transaction = PurchaseTransactionDTO.from_json_api(id, _type, attributes, relationships)

    assert transaction.id == id
    assert transaction.attributes["interchange"] == 2.43
    assert transaction.attributes["ecommerce"] is False
    assert transaction.attributes["recurring"] is False
    assert transaction.attributes["cardPresent"] is True
    assert transaction.attributes["cardNetwork"] == "Visa"
    assert transaction.attributes["digitalWallet"] == "Apple"
    assert transaction.attributes["paymentMethod"] == "Contactless"

def test_list_and_get_transactions_with_type():
    transaction_ids = []
    response = client.transactions.list(ListTransactionParams(100, 0, type=["Fee", "ReceivedAch"]))

    for t in response.data:
        assert t.type == "receivedAchTransaction" or t.type == "feeTransaction"
        transaction_ids.append(t.id)

    for id in transaction_ids:
        response = client.transactions.get(id)
        assert response.data.type == "receivedAchTransaction" or response.data.type == "feeTransaction"


def test_codecs_transactions():
    import inspect
    import unit.models.transaction as foo

    classes = []

    p = 'unit.models.transaction.'
    for name, obj in inspect.getmembers(foo):
        if inspect.isclass(obj):
            try:
                s = str(obj)
                if 'Transaction' in s and 'DTO' in s and 'Base' not in s:
                    i = s.index(p) + len(p)
                    j = s.index('DTO\'>')
                    classes.append(s[i:j])
            except e:
                print(e)
                continue


    transactions = [x.lower() for x in mappings if "Transaction" in x]
    for c in classes:
        if c.lower() not in transactions:
            assert False
