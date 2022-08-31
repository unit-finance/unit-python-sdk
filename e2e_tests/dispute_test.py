import os
from unit import Unit
from unit.models.codecs import DtoDecoder

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def test_dispute_dto():
    dispute_api_response = {
        "type": "dispute",
        "id": "36",
        "attributes": {
          "source": "DebitCard",
          "status": "ResolvedWon",
          "statusHistory": [
            {
              "type": "InvestigationStarted",
              "updatedAt": "2022-02-23T12:15:47.386Z"
            },
            {
              "type": "ResolvedWon",
              "updatedAt": "2022-02-23T13:11:19.210Z"
            }
          ],
          "description": "Debit card transaction",
          "createdAt": "2022-02-23T12:15:47.386Z",
          "amount": 5000,
          "decisionReason": None
        },
        "relationships": {
          "customer": {
            "data": {
              "type": "customer",
              "id": "10001"
            }
          },
          "account": {
            "data": {
              "type": "account",
              "id": "10002"
            }
          },
          "transaction": {
            "data": {
              "type": "transaction",
              "id": "10003"
            }
          }
        }
      }

    id = dispute_api_response["id"]
    attributes = dispute_api_response["attributes"]
    _type = dispute_api_response["type"]

    dispute = DtoDecoder.decode(dispute_api_response)

    assert dispute.id == id
    assert dispute.attributes["amount"] == attributes["amount"]


def test_list_disputes():
    disputes_ids = []
    response = client.disputes.list()
    for c in response.data:
        assert c.type == "dispute"
        disputes_ids.append(c.id)

    for id in disputes_ids:
        response = client.disputes.get(id)
        assert response.data.type == "dispute"


test_dispute_dto()

