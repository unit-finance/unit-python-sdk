import os
import pytest
import requests

from e2e_tests.helpers.helpers import create_counterparty_dto, create_relationship, create_relationships_dict, \
    create_wire_counterparty_dto
from e2e_tests.counterparty_test import create_counterparty
from unit import Unit, Configuration
from unit.models.codecs import DtoDecoder
from unit.models.payment import *
from e2e_tests.account_test import create_deposit_account


token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def create_book_payment_request():
    account_id1 = create_deposit_account().data.id
    account_id2 = create_deposit_account().data.id

    return CreateBookPaymentRequest(200, "Book payment", {"account": Relationship("depositAccount", account_id1),
                                                          "counterpartyAccount": Relationship("depositAccount",
                                                                                              account_id2)},
                                    tags={"purpose": "checking"})


@pytest.fixture
def book_payment():
    request = create_book_payment_request()
    return client.payments.create(request).data


@pytest.fixture
def inline_ach_payment():
    account_id = create_deposit_account().data.id

    data = {
        "data": {
            "type": "wirePayment",
            "attributes": {
                "amount": 500000,
                "description": "Wire Payment from Sandbox"
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

    response = requests.post(f"https://api.s.unit.sh/sandbox/wire-payments", data=json.dumps(data),
                             headers=Configuration("https://api.s.unit.sh", token).get_headers())

    assert response.status_code == 201

    request = CreateInlinePaymentRequest(100, "Funding", create_counterparty_dto("812345673", "12345569", "Checking",
                                                                                 "Jane Doe"),
                                         create_relationship("depositAccount", account_id, "account"))
    return client.payments.create(request).data


@pytest.fixture()
def linked_ach_payment():
    account_id = create_deposit_account().data.id
    counterparty_id = create_counterparty().data.id
    relationships_list = [create_relationship("depositAccount", account_id, "account"),
                          create_relationship("counterparty", counterparty_id)]
    relationships = create_relationships_dict(relationships_list)
    request = CreateLinkedPaymentRequest(10000, "Funding", relationships)
    return client.payments.create(request).data


def test_create_inline_ach_payment(inline_ach_payment):
    assert inline_ach_payment.type == "achPayment"


def test_create_linked_ach_payment(linked_ach_payment):
    assert linked_ach_payment.type == "achPayment"


def test_create_wire_payment():
    account_id = create_deposit_account().data.id
    address = Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500", "US")
    request = CreateWirePaymentRequest(200, "Wire payment", create_wire_counterparty_dto("812345678", "1000000001",
                                                                                         "April Oniel", address),
                                       create_relationship("depositAccount", account_id, "account"), direction="Credit")
    response = client.payments.create(request)
    assert response.data.type == "wirePayment"


def test_list_and_get_payments():
    payments_ids = []

    response = client.payments.list()

    for t in response.data:
        assert "Payment" in t.type
        payments_ids.append(t.id)

    for id in payments_ids:
        response = client.payments.get(id)
        assert "Payment" in response.data.type


def test_list_and_get_payments_filter_by_type():
    payments_ids = []
    params = ListPaymentParams(type=["AchPayment", "WirePayment"])
    response = client.payments.list(params)

    for t in response.data:
        assert t.type == "achPayment" or t.type == "wirePayment"
        payments_ids.append(t.id)

    for id in payments_ids:
        response = client.payments.get(id)
        assert response.data.type == "achPayment" or response.data.type == "wirePayment"


def test_list_and_get_payments_filter_by_status():
    payments_ids = []
    params = ListPaymentParams(status=["Pending", "Sent"])
    response = client.payments.list(params)

    for t in response.data:
        assert t.attributes["status"] == "Pending" or t.attributes["status"] == "Sent"
        payments_ids.append(t.id)

    for id in payments_ids:
        response = client.payments.get(id)
        assert response.data.attributes["status"] == "Pending" or response.data.attributes["status"] == "Sent"


def test_create_book_payment(book_payment):
    assert book_payment.type == "bookPayment"


def test_update_book_payment(book_payment):
    payment_id = book_payment.id
    tags = {"purpose": "test"}
    request = PatchBookPaymentRequest(payment_id, tags)
    response = client.payments.update(request)
    assert response.data.type == "bookPayment"


def test_ach_received_payment_dto():
    ach_received_payment_response_json_api = {
          "type": "achReceivedPayment",
          "id": "1337",
          "attributes": {
            "createdAt": "2022-02-01T12:03:14.406Z",
            "status": "Completed",
            "wasAdvanced": True,
            "isAdvanceable": True,
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


def test_create_bulk_payments():
    payment1 = create_book_payment_request().to_json_api(False)
    payment2 = create_book_payment_request().to_json_api(False)

    response = client.payments.create_bulk([payment1, payment2])
    assert response.data.type == "bulkPayments"
    assert response.data.attributes.get("bulkId") is not None


def test_cancel_ach_payment(inline_ach_payment):
    assert inline_ach_payment.type == "achPayment"
    response = client.payments.cancel(inline_ach_payment.id)
    assert response.data.type == "achPayment"
    assert response.data.id == inline_ach_payment.id
    assert response.data.attributes["amount"] == inline_ach_payment.attributes["amount"]
    assert response.data.attributes["status"] == "Canceled"
