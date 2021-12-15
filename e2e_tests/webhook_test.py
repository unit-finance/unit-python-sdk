import os
import unittest
from unit import Unit
from unit.models.webhook import *
from unit.models.event import BaseEvent


class WebhookE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_verify_webhook(self):
        payload = {"data": [{"id": "613457", "type": "authorizationRequest.pending",
                             "attributes": {"createdAt":"2021-12-15T10:21:59.873Z", "amount": 2500, "available": 0,
                                            "status":"Pending","partialApprovalAllowed": True,
                                            "merchant": {"name": "Apple Inc.", "type": "1000"}, "recurring": False},
                             "relationships":
                                 {"authorizationRequest": {"data": {"id": "4474",
                                                                    "type": "purchaseAuthorizationRequest"}},
                                  "account": {"data": {"id": "49228", "type":"account"}},
                                  "customer": {"data": {"id": "49430", "type": "customer"}},
                                  "card": {"data": {"id": "26068", "type": "card"}}}}]}
        res = self.client.webhooks.verify("kw+Zx3UcAWL/ujc1Px46GGzo0Gc=", "MyToken", payload)
        self.assertTrue(res)

    def create_webhook(self):
        request = CreateWebhookRequest("test", "https://webhook.site/81ee6b53-fde4-4b7d-85a0-0b6249a4488d", "MyToken",
                                       "Json")
        return self.client.webhooks.create(request).data

    def test_create_webhook(self):
        w = self.create_webhook()
        self.assertTrue(w.type == "webhook")

    def test_list_and_get_webhooks(self):
        webhook_ids = []
        response = self.client.webhooks.list()

        for w in response.data:
            self.assertTrue(w.type == "webhook")
            webhook_ids.append(w.id)

        for id in webhook_ids:
            response = self.client.webhooks.get(id)
            self.assertTrue(response.data.type == "webhook")

    def test_update_webhook(self):
        w = self.create_webhook()
        request = PatchWebhookRequest(w.id, "MyLabel")
        response = self.client.webhooks.update(request)
        self.assertTrue(response.data.type == "webhook")

    def test_enable_webhook(self):
        w = self.create_webhook()
        response = self.client.webhooks.enable(w.id)
        self.assertTrue(response.data.type == "webhook" and response.data.attributes["status"] == "Enabled")

    def test_disable_webhook(self):
        w = self.create_webhook()
        response = self.client.webhooks.disable(w.id)
        self.assertTrue(response.data.type == "webhook" and response.data.attributes["status"] == "Disabled")


if __name__ == '__main__':
    unittest.main()
