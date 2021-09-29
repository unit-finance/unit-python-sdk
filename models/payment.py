import json
from datetime import datetime, date
from typing import Literal, Optional
from utils import date_utils
from models import *

AchStatus = Literal["Pending", "Rejected", "Clearing", "Sent", "Canceled", "Returned"]

class BasePayment(object):
    def __init__(self, id: str, created_at: datetime, direction: str, description: str, amount: int,
                 reason: Optional[str], tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.created_at = created_at
        self.direction = direction
        self.description = description
        self.amount = amount
        self.reason = reason
        self.tags = tags
        self.relationships = relationships


class AchPaymentDTO(BasePayment):
    def __init__(self, id: str, created_at: datetime, status: AchStatus, counterparty: Counterparty, direction: str,
                 description: str, amount: int, addenda: Optional[str], reason: Optional[str],
                 settlement_date: Optional[datetime], tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        BasePayment.__init__(self, id, created_at, direction, description, amount, reason, tags, relationships)
        self.type = 'achPayment'
        self.status = status
        self.counterparty = counterparty
        self.addenda = addenda
        self.settlement_date = settlement_date

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        settlement_date = date_utils.to_date(attributes.get("settlementDate")) if attributes.get("settlementDate") else None
        return AchPaymentDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                             attributes["counterparty"], attributes["direction"], attributes["description"],
                             attributes["amount"], attributes.get("addenda"), attributes.get("reason"), settlement_date,
                             attributes.get("tags"), relationships)

class BookPaymentDTO(BasePayment):
    def __init__(self, id: str, created_at: datetime, status: str, direction: Optional[str], description: str, amount: int,
                 reason: Optional[str], tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        BasePayment.__init__(self, id, created_at, direction, description, amount, reason, tags, relationships)
        self.type = 'bookPayment'
        self.status = status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BookPaymentDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                              attributes.get("direction"), attributes["description"], attributes["amount"],
                              attributes.get("reason"), attributes.get("tags"), relationships)

class WirePaymentDTO(BasePayment):
    def __init__(self, id: str, created_at: datetime, status: AchStatus, counterparty: WireCounterparty, direction: str,
                 description: str, amount: int, reason: Optional[str], tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        BasePayment.__init__(self, id, created_at, direction, description, amount, reason, tags, relationships)
        self.type = 'wirePayment'
        self.status = status
        self.counterparty = counterparty
        self.addenda = addenda
        self.settlement_date = settlement_date

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return WirePaymentDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                              WireCounterparty.from_json_api(attributes["counterparty"]), attributes["direction"],
                              attributes["description"], attributes["amount"], attributes.get("reason"),
                              attributes.get("tags"), relationships)

PaymentDTO = Union[AchPaymentDTO, BookPaymentDTO, WirePaymentDTO]

