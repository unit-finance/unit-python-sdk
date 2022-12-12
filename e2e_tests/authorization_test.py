import os
import unittest
from unit import Unit
from unit.models.authorization import *
from unit.models.codecs import DtoDecoder

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def test_list_and_get_authorization_include_non_authorized():
    authorizations = client.authorizations.list()
    for authorization in authorizations.data:
        response = client.authorizations.get(authorization.id, True)
        assert response.data.type == "authorization"

def test_list_and_get_with_filter_by_status():
    params = ListAuthorizationParams(status="Authorized")
    authorizations = client.authorizations.list(params)

    for authorization in authorizations.data:
        response = client.authorizations.get(authorization.id)
        assert response.data.attributes["status"] == "Authorized"

def test_list_with_non_authorized():
    params = ListAuthorizationParams(include_non_authorized=True)
    authorizations = client.authorizations.list(params)

    for authorization in authorizations.data:
        response = client.authorizations.get(authorization.id)
        assert response.data.attributes["status"] == "Authorized"

def test_list_and_get_authorization():
    authorizations = client.authorizations.list()
    for authorization in authorizations.data:
        response = client.authorizations.get(authorization.id)
        assert response.data.type == "authorization"

def test_list_with_parameters():
    params = ListAuthorizationParams(10, 0, sort="-createdAt")
    authorizations = client.authorizations.list(params)
    for authorization in authorizations.data:
        response = client.authorizations.get(authorization.id)
        assert response.data.type == "authorization"

def test_list_with_wrong_parameters():
    params = ListAuthorizationParams(10, 0, "", "-1", include_non_authorized=False)
    response = client.authorizations.list(params)
    assert response.data == []

def test_authorization_api_response():
    authorization_api_response = {
      "type": "authorization",
      "id": "97",
      "attributes": {
        "createdAt": "2021-02-21T07:29:42.447Z",
        "amount": 2000,
        "cardLast4Digits": "0019",
        "status": "Declined",
        "declineReason": "Declined for test",
        "merchant": {
          "name": "Europcar Mobility Group",
          "type": 3381,
          "category": "EUROP CAR",
          "location": "Cupertino, CA",
          "id": "029859000085093"
        },
        "recurring": False,
        "paymentMethod": "Contactless",
        "digitalWallet": "Apple",
        "cardVerificationData": {
          "verificationMethod": "CVV2"
        },
        "cardNetwork": "Visa",
        "paymentMethod": "Swipe",
        "digitalWallet": "Google",
        "cashWithdrawalAmount": 150
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
            "id": "10501"
          }
        }
      }
    }

    _id = authorization_api_response["id"]
    _type = authorization_api_response["type"]
    _attributes = authorization_api_response["attributes"]

    authorization = DtoDecoder.decode(authorization_api_response)
    dto_attributes = authorization.attributes

    assert authorization.id == _id
    assert authorization.type == _type
    for a_name in _attributes.keys():
        a_value = dto_attributes.get(a_name)
        if type(a_value) == datetime:
            continue

        assert a_value == _attributes.get(a_name)

