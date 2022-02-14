import os
import unittest
from unit import Unit
from unit.models.authorization import *


class AuthorizationsE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_list_and_get_authorization(self):
        authorizations = self.client.authorizations.list()
        for authorization in authorizations.data:
            response = self.client.authorizations.get(authorization.id, True)
            self.assertTrue(response.data.type == "authorization")

    def test_list_and_get_with_filter_by_status(self):
        params = ListAuthorizationParams(status="Authorized")
        authorizations = self.client.authorizations.list(params)

        for authorization in authorizations.data:
            response = self.client.authorizations.get(authorization.id)
            self.assertTrue(response.data.attributes["status"] == "Authorized")

    def test_list_with_non_authorized(self):
        params = ListAuthorizationParams(include_non_authorized=True)
        authorizations = self.client.authorizations.list(params)

        for authorization in authorizations.data:
            response = self.client.authorizations.get(authorization.id)
            self.assertTrue(response.data.attributes["status"] == "Authorized")

    def test_list_with_parameters(self):
        params = ListAuthorizationParams(10, 0, "", "49423")
        authorizations = self.client.authorizations.list(params)
        for authorization in authorizations.data:
            response = self.client.authorizations.get(authorization.id)
            self.assertTrue(response.data.type == "authorization")

    def test_list_with_wrong_parameters(self):
        params = ListAuthorizationParams(10, 0, "", "-1", include_non_authorized=False)
        response = self.client.authorizations.list(params)
        self.assertTrue(response.data == [])


if __name__ == '__main__':
    unittest.main()

