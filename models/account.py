import json
from datetime import datetime, date
from typing import Literal, Optional
from utils import date_utils

from models import *

AccountStatus = Literal["Open", "Closed"]
CloseReason = Literal["ByCustomer", "Fraud"]


class DepositAccountDTO(object):
    def __init__(self, id: str, created_at: datetime, name: str, deposit_product: str, routing_number: str,
                 account_number: str, currency: str, balance: int, hold: int, available: int, status: AccountStatus,
                 tags: Optional[dict[str, str]], close_reason: Optional[CloseReason],
                 relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = "depositAccount"
        self.created_at = created_at
        self.name = name
        self.deposit_product = deposit_product
        self.routing_number = routing_number
        self.account_number = account_number
        self.currency = currency
        self.balance = balance
        self.hold = hold
        self.available = available
        self.tags = tags
        self.status = status
        self.close_reason = close_reason
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DepositAccountDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["name"], attributes["depositProduct"],
            attributes["routingNumber"], attributes["accountNumber"], attributes["currency"], attributes["balance"],
            attributes["hold"], attributes["available"],attributes["status"], attributes.get("tags"),
            attributes.get("closeReason"), relationships
        )


AccountDTO = Union[DepositAccountDTO]

class CreateDepositAccountRequest(UnitRequest):
    def __init__(self, deposit_product: str, relationships: Optional[dict[str, Relationship]],
                 tags: Optional[dict[str, str]] = None, idempotency_key: Optional[str] = None):
        self.deposit_product = deposit_product
        self.tags = tags
        self.idempotency_key = idempotency_key
        self.relationships = relationships

    def to_json_api(self) -> dict:
        payload = {
            "data": {
                "type": "depositAccount",
                "attributes": {
                    "depositProduct": self.deposit_product,
                },
                "relationships": self.relationships
            }
        }

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        if self.idempotency_key:
            payload["data"]["attributes"]["idempotencyKey"] = self.idempotency_key

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class PatchDepositAccountRequest(UnitRequest):
    def __init__(self, account_id: str, deposit_product: Optional[str] = None, tags: Optional[dict[str, str]] = None):
        self.account_id = account_id
        self.deposit_product = deposit_product
        self.tags = tags

    def to_json_api(self) -> dict:
        payload = {
            "data": {
                "type": "depositAccount",
                "attributes": {}
            }
        }

        if self.deposit_product:
            payload["data"]["attributes"]["depositProduct"] = self.deposit_product

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())

class AccountLimitsDTO(object):
    def __init__(self, ach: object, card: object):
        self.type = "limits"
        self.ach = ach
        self.card = card

    @staticmethod
    def from_json_api(_type, attributes):
        return AccountLimitsDTO(attributes["ach"], attributes["card"])

