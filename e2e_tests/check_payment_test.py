import os

from e2e_tests.helpers.helpers import create_relationship, generate_uuid, create_deposit_account, \
    create_individual_customer
from unit import Unit
from unit.models import Address
from unit.models.check_payment import CheckPaymentDTO, CreateCheckPaymentRequest, CheckPaymentCounterparty
from unit.models.event import CheckPaymentPendingEvent

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def test_check_payment_from_json():
    data = {
      "type": "checkPayment",
      "id": "3",
      "attributes": {
        "createdAt": "2023-02-21T11:31:03.704Z",
        "updatedAt": "2023-02-21T11:31:03.704Z",
        "amount": 10000,
        "sendAt": "2023-09-10T12:50:00.704Z",
        "description": "Check Payment | 0322",
        "status": "Processed",
        "deliveryStatus": "Delivered",
        "trackedAt": "2023-02-23T11:31:03.704Z",
        "postalCode": "94303",
        "checkNumber": "0322",
        "onUsAuxiliary": "0322",
        "onUs": "864800000002/",
        "counterparty": {
          "name": "John Doe",
          "address": {
            "street": "5230 Newell Rd",
            "city": "Palo Alto",
            "state": "CA",
            "postalCode": "94303"
          }
        },
        "counterpartyRoutingNumber": "051402372",
        "returnCutoffTime": "2023-03-23T15:50:00.000Z",
        "additionalVerificationStatus": "Required"
      },
      "relationships": {
        "account": {
          "data": {
            "type": "account",
            "id": "75002"
          }
        },
        "customer": {
          "data": {
            "type": "customer",
            "id": "100425"
          }
        },
        "customers": {
          "data": [
            {
              "type": "customer",
              "id": "10001"
            }
          ]
        },
        "transaction": {
          "data": {
            "type": "transaction",
            "id": "123423"
          }
        }
      }
    }

    obj = CheckPaymentDTO.from_json_api(data["id"], data["type"], data["attributes"], data["relationships"])
    assert obj.id == data["id"]


def test_list_check_payment():
    res = client.check_payments.list()
    for p in res.data:
        assert p.type == "checkPayment"


def test_list_and_get_check_payment():
    res = client.check_payments.list()
    for p in res.data:
        assert p.type == "checkPayment"

        get_res = client.check_payments.get(p.id).data
        assert p.id == get_res.id
        assert p.type == get_res.type


def test_create_check_payment():
    created_account = create_deposit_account(client)
    account_id = created_account.data.id
    customer_id = created_account.data.relationships.get("customer").id

    account = create_relationship("depositAccount", account_id, "account")
    customer = create_relationship("customer", customer_id)

    relationships = {}
    relationships.update(account)
    relationships.update(customer)

    req = CreateCheckPaymentRequest(100, CheckPaymentCounterparty("John Doe",
                                                                  Address("5230 Newell Rd", "Palo Alto", "CA", "94303",
                                                                          "US")), "test create checkPayment",
                                    relationships, send_date="2023-09-10", idempotency_key=generate_uuid())

    res = client.check_payments.create(req)
    assert True


def test_check_payment_event():
    data = {
      "id": "376",
      "type": "checkPayment.pending",
      "attributes": {
        "createdAt": "2021-06-06T07:21:39.509Z",
        "status": "Pending",
        "previousStatus": "New",
        "counterpartyMoved": True
      },
      "relationships": {
        "checkPayment": {
          "data": {
            "id": "122",
            "type": "checkPayment"
          }
        },
        "account": {
          "data": {
            "id": "10001",
            "type": "account"
          }
        },
        "customer": {
          "data": {
            "id": "10000",
            "type": "customer"
          }
        }
      }
    }

    event = CheckPaymentPendingEvent.from_json_api(data["id"],data["type"],data["attributes"],data["relationships"])
    x = 6