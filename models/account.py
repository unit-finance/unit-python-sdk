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

