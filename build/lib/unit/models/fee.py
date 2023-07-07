import json
from typing import Optional
from unit.models import *


class FeeDTO(object):
    def __init__(self, id: str, amount: int, description: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "fee"
        self.attributes = {"amount": amount, "description": description, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return FeeDTO(_id, attributes["amount"], attributes["description"], attributes.get("tags"), relationships)


class CreateFeeRequest(object):
    def __init__(self, amount: int, description: str, relationships: Optional[Dict[str, Relationship]],
                 tags: Optional[Dict[str, str]] = None, idempotency_key: Optional[str] = None):
        self.amount = amount
        self.description = description
        self.tags = tags
        self.idempotency_key = idempotency_key
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "fee",
                "attributes": {
                    "amount": self.amount,
                    "description": self.description
                },
                "relationships": self.relationships
            }
        }

        if self.idempotency_key:
            payload["data"]["attributes"]["idempotencyKey"] = self.tags

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())

