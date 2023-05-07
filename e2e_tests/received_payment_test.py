import json
import os
import pytest
import requests

from e2e_tests.helpers.helpers import create_deposit_account
from unit import Unit
from unit.models.codecs import UnitEncoder, DtoDecoder
from unit.models.received_payment import ListReceivedPaymentParams, PatchReceivedPaymentRequest

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


@pytest.fixture(autouse=True)
def simulate_received_payment():
    headers = {
            "content-type": "application/vnd.api+json",
            "authorization": f"Bearer {token}",
            "user-agent": "unit-python-sdk"
    }

    account_id = create_deposit_account(client).data.id

    data = {
        "data": {
            "type": "achReceivedPayment",
            "attributes": {
                "amount": 10000,
                "description": "paycheck simulation Sandbox",
                "companyName": "UBER LTD",
                "completionDate": "2020-07-30",
                "secCode": "PPD"
            },
            "relationships": {
                "account": {
                    "data": {
                        "type": "depositAccount",
                        "id": account_id
                    }
                }
            }
        }
      }

    res = requests.post(f"https://api.s.unit.sh/sandbox/received-payments", data=json.dumps(data, cls=UnitEncoder),
                        headers=headers)

    if res.status_code != 201:
        print("Failed to simulate received payment")


def test_ach_received_payment_dto():
    ach_received_payment_response_json_api = {
      "data": {
        "type": "achReceivedPayment",
        "id": "1337",
        "attributes": {
          "createdAt": "2022-02-01T12:03:14.406Z",
          "status": "Pending",
          "wasAdvanced": False,
          "amount": 500000,
          "completionDate": "2020-07-30",
          "companyName": "UBER LTD",
          "counterpartyRoutingNumber": "051402372",
          "description": "Sandbox",
          "traceNumber": "123456789123456",
          "secCode": "PPD"
        },
        "relationships": {
          "account": {
            "data": {
              "type": "account",
              "id": "163555"
            }
          },
          "customer": {
            "data": {
              "type": "customer",
              "id": "129522"
            }
          }
        }
      }
    }

    _id = ach_received_payment_response_json_api["id"]
    attributes = ach_received_payment_response_json_api["attributes"]
    _type = ach_received_payment_response_json_api["type"]

    payment = DtoDecoder.decode(ach_received_payment_response_json_api)

    assert payment.id == _id
    assert str(payment.attributes["completionDate"]) == attributes["completionDate"]
    assert payment.attributes["traceNumber"] == attributes["traceNumber"]


def test_ach_received_payment_dto():
    ach_received_payment_response_json_api = {
          "type": "achReceivedPayment",
          "id": "1337",
          "attributes": {
            "createdAt": "2022-02-01T12:03:14.406Z",
            "status": "Completed",
            "wasAdvanced": True,
            "amount": 100000,
            "completionDate": "2022-01-23",
            "companyName": "Uber",
            "counterpartyRoutingNumber": "051402372",
            "description": "Sandbox Transaction",
            "traceNumber": "123456789123456",
            "secCode": "PPD",
            "tags": {}
          },
          "relationships": {
            "account": {
              "data": {
                "type": "account",
                "id": "163555"
              }
            },
            "customer": {
              "data": {
                "type": "customer",
                "id": "129522"
              }
            },
            "receivePaymentTransaction": {
              "data": {
                "type": "transaction",
                "id": "101"
              }
            },
            "paymentAdvanceTransaction": {
              "data": {
                "type": "transaction",
                "id": "202"
              }
            },
            "repayPaymentAdvanceTransaction": {
              "data": {
                "type": "transaction",
                "id": "890"
              }
            }
          }
        }

    _id = ach_received_payment_response_json_api["id"]
    attributes = ach_received_payment_response_json_api["attributes"]
    _type = ach_received_payment_response_json_api["type"]

    payment = DtoDecoder.decode(ach_received_payment_response_json_api)

    assert payment.id == _id
    assert str(payment.attributes["completionDate"]) == attributes["completionDate"]


def test_list_payments():
    response = client.received_payments.list(ListReceivedPaymentParams(limit=150, offset=1,
                                                                       status=["Pending", "Advanced", "Completed"]))

    for t in response.data:
        assert t.type == "achReceivedPayment"


def test_list_and_get_payments():
    payments_ids = []

    response = client.received_payments.list()

    for t in response.data:
        assert t.type == "achReceivedPayment"
        payments_ids.append(t.id)

    for _id in payments_ids:
        response = client.received_payments.get(_id, "customer,account")
        assert response.data.type == "achReceivedPayment"
        assert response.included
        assert len(response.included) == 2
        assert any("Account" in x.type for x in response.included)
        assert any("Customer" in x.type for x in response.included)


def test_list_and_update_payments():
    response = client.received_payments.list()

    for t in response.data:
        assert t.type == "achReceivedPayment"
        payment = client.received_payments.update(PatchReceivedPaymentRequest(t.id, {"by": "Test",
                                                                                     "test": "test"})).data
        assert payment.type == "achReceivedPayment"
        assert payment.attributes.get("tags")
        assert payment.attributes.get("tags").get("by") == "Test"


def test_advance_payments():
    response = client.received_payments.list()
    pending_received_payments = list(filter(lambda p: p.attributes.get("status") == "Pending", response.data))

    for t in pending_received_payments:
        payment = client.received_payments.advance(t.id).data
        assert payment.id == t.id
        assert payment.attributes.get("status") == "Advanced"

