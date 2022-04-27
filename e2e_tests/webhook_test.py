import os
import unittest
from unit import Unit
from unit.models.webhook import *
from unit.models.event import BaseEvent

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def create_webhook():
    request = CreateWebhookRequest("test", "https://webhook.site/81ee6b53-fde4-4b7d-85a0-0b6249a4488d", "MyToken",
                                   "Json")
    return client.webhooks.create(request).data

def test_create_webhook():
    w = create_webhook()
    assert w.type == "webhook"

def test_list_and_get_webhooks():
    webhook_ids = []
    response = client.webhooks.list()

    for w in response.data:
        assert w.type == "webhook"
        webhook_ids.append(w.id)

    for id in webhook_ids:
        response = client.webhooks.get(id)
        assert response.data.type == "webhook"

def test_update_webhook():
    w = create_webhook()
    request = PatchWebhookRequest(w.id, "MyLabel")
    response = client.webhooks.update(request)
    assert response.data.type == "webhook"

def test_enable_webhook():
    w = create_webhook()
    response = client.webhooks.enable(w.id)
    assert response.data.type == "webhook" and response.data.attributes["status"] == "Enabled"

def test_disable_webhook():
    w = create_webhook()
    response = client.webhooks.disable(w.id)
    assert response.data.type == "webhook" and response.data.attributes["status"] == "Disabled"

def test_verify_webhook():
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
    res = client.webhooks.verify("kw+Zx3UcAWL/ujc1Px46GGzo0Gc=", "MyToken", payload)
    assert res
