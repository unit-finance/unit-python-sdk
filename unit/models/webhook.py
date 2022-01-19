import json
from datetime import datetime, date
from unit.utils import date_utils
from unit.models import *
from typing import Literal

ContentType = Literal["Json", "JsonAPI"]
WebhookStatus = Literal["Enabled", "Disabled"]


class WebhookDTO(object):
    def __init__(self, id: str, created_at: datetime, label: str, url: str, status: WebhookStatus,
                 content_type: ContentType, token: str):
        self.id = id
        self.type = 'webhook'
        self.attributes = {"createdAt": created_at, "label": label, "url": url, "status": status,
                           "contentType": content_type, "token": token}

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return WebhookDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["label"], attributes["url"],
            attributes["status"], attributes["contentType"], attributes["token"])


class CreateWebhookRequest(object):
    def __init__(self, label: str, url: str, token: str, content_type: ContentType):
        self.label = label
        self.url = url
        self.token = token
        self.content_type = content_type

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "webhook",
                "attributes": {
                    "label": self.label,
                    "url": self.url,
                    "token": self.token,
                    "contentType": self.content_type
                }
            }
        }

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class PatchWebhookRequest(object):
    def __init__(self, webhook_id: str, label: Optional[str] = None, url: Optional[str] = None,
                 content_type: Optional[ContentType] = None, token: Optional[str] = None):
        self.webhook_id = webhook_id
        self.label = label
        self.url = url
        self.content_type = content_type
        self.token = token

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "webhook",
                "attributes": {}
            }
        }

        if self.label:
            payload["data"]["attributes"]["label"] = self.label

        if self.url:
            payload["data"]["attributes"]["url"] = self.url

        if self.content_type:
            payload["data"]["attributes"]["contentType"] = self.content_type

        if self.token:
            payload["data"]["attributes"]["token"] = self.token

        return payload


class ListWebhookParams(UnitParams):
    def __init__(self, limit: int = 100, offset: int = 0):
        self.limit = limit
        self.offset = offset

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        return parameters

