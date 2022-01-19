import os
import unittest
from unit import Unit
from unit.models.api_token import CreateAPITokenRequest


class APITokenE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)
    user_id = "252"

    def create_api_token(self):
        request = CreateAPITokenRequest(self.user_id, "Test token", "customers applications", "2022-07-01T13:47:17.000Z")
        return self.client.api_tokens.create(request).data

    def test_list_api_tokens(self):
        api_tokens_ids = []
        response = self.client.api_tokens.list(self.user_id)

        for t in response.data:
            self.assertTrue(t.type == "apiToken")

    def test_create_api_token(self):
        token = self.create_api_token()
        self.assertTrue(token.type == "apiToken")

    def test_delete_api_token(self):
        token = self.create_api_token()
        response = self.client.api_tokens.revoke(self.user_id, token.id)
        self.assertTrue(response.data == [])
