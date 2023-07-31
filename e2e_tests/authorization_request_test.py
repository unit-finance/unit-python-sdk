import os
import unittest
from unit import Unit
from unit.models.authorization_request import *

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

#
# def test_decline_request():
#     request = DeclineAuthorizationRequest("3722", "ReferToCardIssuer")
#     response = client.authorization_requests.decline(request)
#     assert response.data.type == "purchaseAuthorizationRequest"
