import json
from datetime import datetime, date
from typing import Literal, Optional
from utils import date_utils
from models import *

class BaseTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.tags = tags
        self.relationships = relationships

class OriginatedAchTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, description: str, counterparty: Counterparty, tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'originatedAchTransaction'
        self.description = description
        self.counterparty = counterparty

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return OriginatedAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["description"],
            Counterparty.from_json_api(attributes["counterparty"]), attributes.get("tags"), relationships)


class ReceivedAchTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, description: str, addenda: Optional[str], company_name: str,
                 counterparty_routing_number: str, trace_number: Optional[str], sec_code: Optional[str],
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'receivedAchTransaction'
        self.description = description
        self.addenda = addenda
        self.company_name = company_name
        self.counterparty_routing_number = counterparty_routing_number
        self.trace_number = trace_number
        self.sec_code = sec_code

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReceivedAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["description"],
            attributes.get("addenda"), attributes["companyName"], attributes["counterpartyRoutingNumber"],
            attributes.get("traceNumber"), attributes.get("secCode"), attributes.get("tags"), relationships)


class ReturnedAchTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, company_name: str, counterparty_name: str, counterparty_routing_number: str, reason: str,
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'returnedAchTransaction'
        self.addenda = addenda
        self.company_name = company_name
        self.counterparty_routing_number = counterparty_routing_number
        self.reason = reason

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReturnedAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["companyName"],
            attributes["counterpartyName"], attributes["counterpartyRoutingNumber"], attributes["reason"],
            attributes.get("tags"), relationships)


class ReturnedReceivedAchTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 company_name: str, reason: str, tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'returnedReceivedAchTransaction'
        self.company_name = company_name
        self.reason = reason

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReturnedReceivedAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["companyName"],
            attributes["reason"], attributes.get("tags"), relationships)


class DishonoredAchTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 company_name: str, counterparty_routing_number: str, trace_number: str, reason: str,
                 sec_code: Optional[str], tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'dishonoredAchTransaction'
        self.company_name = company_name
        self.counterparty_routing_number = counterparty_routing_number
        self.trace_number = trace_number
        self.reason = reason
        self.sec_code = sec_code

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DishonoredAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["companyName"],
            attributes["counterpartyRoutingNumber"], attributes["traceNumber"], attributes["reason"],
            attributes.get("secCode"), attributes.get("tags"), relationships)


class BookTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, description: str, addenda: Optional[str], counterparty: Counterparty,
                 relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.description = description
        self.type = 'bookTransaction'
        self.counterparty = counterparty

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BookTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"],
            Counterparty.from_json_api(attributes["counterparty"]), relationships)


class PurchaseTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, card_last_4_digits: str, merchant: Merchant, coordinates: Coordinates, recurring: bool,
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'purchaseTransaction'
        self.card_last_4_digits = card_last_4_digits
        self.merchant = merchant
        self.coordinates = coordinates
        self.recurring = recurring

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PurchaseTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["cardLast4Digits"],
            Merchant.from_json_api(attributes["merchant"]), Coordinates.from_json_api(attributes["coordinates"]),
            attributes["recurring"], attributes.get("tags"), relationships)


class AtmTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, card_last_4_digits: str, atm_name: str, atm_location: Optional[str], surcharge: int,
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'atmTransaction'
        self.card_last_4_digits = card_last_4_digits
        self.atm_name = atm_name
        self.atm_location = atm_location
        self.surcharge = recurring

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AtmTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["cardLast4Digits"],
            attributes["atmName"], attributes.get("atmLocation"), attributes["surcharge"], attributes.get("tags"),
                                 relationships)


class FeeTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'feeTransaction'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return FeeTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                 attributes["amount"], attributes["balance"], attributes["summary"],
                                 attributes.get("tags"), relationships)


class CardTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, card_last_4_digits: int, tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'cardTransaction'
        self.card_last_4_digits = card_last_4_digits

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                  attributes["amount"], attributes["balance"], attributes["summary"],
                                  attributes["cardLast4Digits"], attributes.get("tags"), relationships)


class CardReversalTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, card_last_4_digits: int, tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'cardReversalTransaction'
        self.card_last_4_digits = card_last_4_digits

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardReversalTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["cardLast4Digits"],
                                 attributes.get("tags"), relationships)


class WireTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, counterparty: Counterparty, description: str, sender_reference: str,
                 reference_for_beneficiary: str, tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'wireTransaction'
        self.description = description
        self.counterparty = counterparty
        self.description = description
        self.sender_reference = sender_reference
        self.reference_for_beneficiary = reference_for_beneficiary

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return WireTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"],
            Counterparty.from_json_api(attributes["counterparty"]), attributes["description"],
            attributes["senderReference"], attributes["referenceForBeneficiary"], attributes.get("tags"), relationships)


class ReleaseTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, sender_name: str, sender_address: str, sender_account_number: str,
                 counterparty: Counterparty, amount: int, direction: str, description: str, balance: int, summary: str,
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'releaseTransaction'
        self.description = description
        self.sender_name = sender_name
        self.sender_address = sender_address
        self.sender_account_number = sender_account_number
        self.counterparty = counterparty
        self.description = description

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReleaseTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["senderName"],
                                  attributes["senderAddress"], attributes["senderAccountNumber"], attributes["counterparty"],
                                  attributes["amount"], attributes["direction"], attributes["description"],
                                  attributes["balance"], attributes["summary"], attributes.get("tags"), relationships)


class AdjustmentTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 description: str, tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'adjustmentTransaction'
        self.description = description

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AdjustmentTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                  attributes["amount"], attributes["balance"],
                                  attributes["summary"], attributes["description"], attributes.get("tags"), relationships)


class InterestTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'interestTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return InterestTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                      attributes["amount"], attributes["balance"], attributes["summary"],
                                      attributes.get("tags"), relationships)


class DisputeTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, dispute_id: str,
                 summary: str, reason: str, tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'disputeTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.dispute_id = dispute_id
        self.summary = summary
        self.reason = reason
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DisputeTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                  attributes["amount"], attributes["balance"], attributes["disputeId"],
                                  attributes["summary"], attributes["reason"], attributes.get("tags"), relationships)


class CheckDepositTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'checkDepositTransaction'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                          attributes["amount"], attributes["balance"], attributes["summary"],
                                          attributes.get("tags"), relationships)


class ReturnedCheckDepositTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 reason: str, tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self,id,created_at,direction,amount,balance,summary,tags,relationships)
        self.type = 'returnedCheckDepositTransaction'
        self.reason = reason

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReturnedCheckDepositTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                          attributes["amount"], attributes["balance"], attributes["summary"],
                                          attributes["reason"], attributes.get("tags"), relationships)


TransactionDTO = Union[OriginatedAchTransactionDTO, ReceivedAchTransactionDTO, ReturnedAchTransactionDTO,
                       ReturnedReceivedAchTransactionDTO, DishonoredAchTransactionDTO, BookTransactionDTO,
                       PurchaseTransactionDTO, AtmTransactionDTO, FeeTransactionDTO, CardTransactionDTO,
                       CardReversalTransactionDTO, WireTransactionDTO, ReleaseTransactionDTO, AdjustmentTransactionDTO,
                       InterestTransactionDTO, DisputeTransactionDTO, CheckDepositTransactionDTO,
                       ReturnedCheckDepositTransactionDTO]


class PatchTransactionRequest(BaseTransactionDTO):
    def __init__(self, account_id: str, transaction_id: str, tags: Optional[dict[str, str]] = None):
        self.account_id = account_id
        self.transaction_id = transaction_id
        self.tags = tags

    def to_json_api(self) -> dict:
        payload = {
            "data": {
                "type": "transaction",
                "attributes": {}
            }
        }

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

