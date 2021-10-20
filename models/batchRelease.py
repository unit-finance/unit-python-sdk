import json
from datetime import datetime, date
from typing import Literal, Optional
from utils import date_utils
from models import *


class BatchReleaseDTO(object):
    def __init__(self, id: str, amount: int, description: str, sender_name: str, sender_address: Address,
                 sender_account_number: str, relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = "batchRelease"
        self.attributes = {"amount": amount, "description": description, "senderName": sender_name,
                           "senderAddress": sender_address, "senderAccountNumber": sender_account_number}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BatchReleaseDTO(
            _id, attributes["amount"], attributes["description"], attributes["senderName"], attributes["senderAddress"],
            attributes["senderAccountNumber"], relationships)


class CreateBatchReleaseRequest(object):
    def __init__(self, amount: int, description: str, sender_name: str, sender_address: Address,
                 sender_account_number: str, relationships: Optional[dict[str, Relationship]],
                 tags: Optional[dict[str, str]] = None):
        self.amount = amount
        self.description = description
        self.sender_name = sender_name
        self.sender_address = sender_address
        self.sender_account_number = sender_account_number
        self.tags = tags
        self.relationships = relationships

    def to_json_api(self) -> dict:
        payload = {
            "data": {
                "type": "batchRelease",
                "attributes": {
                    "amount": self.amount,
                    "description": self.description,
                    "senderName": self.sender_name,
                    "senderAddress": self.sender_address,
                    "senderAccountNumber": self.sender_account_number
                },
                "relationships": self.relationships
            }
        }

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())

