import os
import unittest
from unit import Unit
from unit.models.authorization_request import *
from unit.models.codecs import DtoDecoder

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def test_list_and_get_authorization_requests():
    authorizations = client.authorization_requests.list()
    for authorization in authorizations.data:
        response = client.authorization_requests.get(authorization.id)
        assert "AuthorizationRequest" in response.data.type

def test_list_with_parameters():
    params = ListPurchaseAuthorizationRequestParams(10, 0)
    authorizations = client.authorization_requests.list(params)
    for authorization in authorizations.data:
        response = client.authorization_requests.get(authorization.id)
        assert "AuthorizationRequest" in response.data.type

def test_list_with_wrong_parameters():
    params = ListPurchaseAuthorizationRequestParams(10, 0, "", "-1")
    response = client.authorization_requests.list(params)
    assert response.data == []

def test_approve_request_payload():
    request_payload = ApproveAuthorizationRequest("3722", 200, {"test": "test"}, "12345").to_json_api()
    assert request_payload["data"]["type"] == "approveAuthorizationRequest"
    assert request_payload["data"]["attributes"]["amount"] == 200
    assert request_payload["data"]["attributes"]["tags"] == {"test": "test"}
    assert request_payload["data"]["attributes"]["fundingAccount"] == "12345"


def test_card_transaction_authorization_request_dto():
    data = {
      "type": "cardTransactionAuthorizationRequest",
      "id": "1",
      "attributes": {
        "createdAt": "2021-06-22T13:39:17.018Z",
        "amount": 2500,
        "status": "Pending",
        "partialApprovalAllowed": False,
        "merchant": {
          "name": "Apple Inc.",
          "type": 1000,
          "category": "",
          "location": "Cupertino, CA",
          "id": "311204598883"
        },
        "recurring": False,
        "paymentMethod": "Contactless",
        "digitalWallet": "Apple",
        "cardVerificationData": {
          "verificationMethod": "CVV2"
        },
        "cardNetwork": "Visa"
      },
      "relationships": {
        "customer": {
          "data": {
            "type": "customer",
            "id": "10000"
          }
        },
        "account": {
          "data": {
            "type": "account",
            "id": "10001"
          }
        },
        "card": {
          "data": {
            "type": "card",
            "id": "7"
          }
        }
      }
    }

    authorization_request = DtoDecoder.decode(data)
    assert type(authorization_request) is CardTransactionAuthorizationRequestDTO
    assert authorization_request.id == data["id"]
    assert authorization_request.type == data["type"]
    assert authorization_request.attributes.get("cardNetwork") == data["attributes"]["cardNetwork"]


def test_atm_authorization_request_dto():
    data = {
        "type": "atmAuthorizationRequest",
        "id": "1",
        "attributes": {
            "createdAt": "2021-06-22T13:39:17.018Z",
            "amount": 2500,
            "status": "Pending",
            "partialApprovalAllowed": False,
            "direction": "Debit",
            "atmName": "HOME FED SAV BK",
            "atmLocation": "Cupertino, CA, US",
            "surcharge": 0,
            "internationalServiceFee": 0,
            "cardNetwork": "Allpoint"
        },
        "relationships": {
            "customer": {
                "data": {
                    "type": "customer",
                    "id": "10000"
                }
            },
            "account": {
                "data": {
                    "type": "account",
                    "id": "10001"
                }
            },
            "card": {
                "data": {
                    "type": "card",
                    "id": "7"
                }
            }
        }
    }

    authorization_request = DtoDecoder.decode(data)
    assert type(authorization_request) is AtmAuthorizationRequestDTO
    assert authorization_request.id == data["id"]
    assert authorization_request.type == data["type"]
    assert authorization_request.attributes.get("cardNetwork") == data["attributes"]["cardNetwork"]


def test_purchase_authorization_request_dto():
    data = {
      "type": "purchaseAuthorizationRequest",
      "id": "1",
      "attributes": {
        "createdAt": "2021-06-22T13:39:17.018Z",
        "amount": 2500,
        "status": "Pending",
        "partialApprovalAllowed": False,
        "merchant": {
          "name": "Apple Inc.",
          "type": 1000,
          "category": "",
          "location": "Cupertino, CA",
          "id": "311204598883"
        },
        "recurring": False,
        "paymentMethod": "Contactless",
        "digitalWallet": "Apple",
        "cardVerificationData": {
          "verificationMethod": "CVV2"
        },
        "ecommerce": False,
        "cardPresent": False,
        "cardNetwork": "Visa"
      },
      "relationships": {
        "customer": {
          "data": {
            "type": "customer",
            "id": "10000"
          }
        },
        "account": {
          "data": {
            "type": "account",
            "id": "10001"
          }
        },
        "card": {
          "data": {
            "type": "card",
            "id": "7"
          }
        }
      }
    }


#
# def test_decline_request():
#     request = DeclineAuthorizationRequest("3722", "ReferToCardIssuer")
#     response = client.authorization_requests.decline(request)
#     assert response.data.type == "purchaseAuthorizationRequest"
