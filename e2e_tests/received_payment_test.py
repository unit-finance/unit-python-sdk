import os
import pytest
import requests

from e2e_tests.helpers.helpers import create_deposit_account
from unit import Unit
from unit.models.codecs import UnitEncoder
from unit.models.payment import *


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

    return ""


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
        response = client.received_payments.get(_id, "customer")
        assert response.data.type == "achReceivedPayment"
        assert response.included


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

