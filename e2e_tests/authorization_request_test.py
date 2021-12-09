import os
import unittest
from unit import Unit
from unit.models.authorization_request import *


class AuthorizationRequestsE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_list_and_get_authorization_requests(self):
        authorizations = self.client.authorization_requests.list()
        for authorization in authorizations.data:
            response = self.client.authorization_requests.get(authorization.id)
            self.assertTrue(response.data.type == "purchaseAuthorizationRequest")

    def test_list_with_parameters(self):
        params = PurchaseAuthorizationRequestListParams(10, 0, "", "49430")
        authorizations = self.client.authorization_requests.list(params)
        for authorization in authorizations.data:
            response = self.client.authorization_requests.get(authorization.id)
            self.assertTrue(response.data.type == "purchaseAuthorizationRequest")

    def test_list_with_wrong_parameters(self):
        params = PurchaseAuthorizationRequestListParams(10, 0, "", "-1")
        response = self.client.authorization_requests .list(params)
        self.assertTrue(response.data == [])

    def test_approve_request(self):
        request = ApproveAuthorizationRequest("3722", 200, {"test": "test"})
        response = self.client.authorization_requests.approve(request)
        self.assertTrue(response.data.type == "purchaseAuthorizationRequest")

    def test_decline_request(self):
        request = DeclineAuthorizationRequest("3722", "ReferToCardIssuer")
        response = self.client.authorization_requests.decline(request)
        self.assertTrue(response.data.type == "purchaseAuthorizationRequest")


if __name__ == '__main__':
    unittest.main()

