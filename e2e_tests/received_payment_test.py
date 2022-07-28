import os
from unit import Unit
from unit.models.payment import AchReceivedPaymentDTO

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def test_received_payment_response():
    ach_received_payment_api_response = {
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
        "description": "Paycheck",
        "traceNumber": "123456789123456",
        "secCode": "PPD"
      },
      "relationships": {
        "account": {
          "data": {
            "type": "account",
            "id": "163575"
          }
        },
        "customer": {
          "data": {
            "type": "customer",
            "id": "129528"
          }
        }
      }
    }

    _id = ach_received_payment_api_response["id"]
    attributes = ach_received_payment_api_response["attributes"]
    relationships = ach_received_payment_api_response["relationships"]
    _type = ach_received_payment_api_response["type"]

    payment = AchReceivedPaymentDTO.from_json_api(_id, _type, attributes, relationships)

    assert payment.id == _id
    assert payment.type == _type
    assert payment.attributes["wasAdvanced"] is False
    assert payment.attributes["traceNumber"] == "123456789123456"
    assert payment.relationships["account"]["data"]["id"] == "163575"
