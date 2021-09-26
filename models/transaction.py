import json
from datetime import datetime, date
from typing import Literal, Optional
from utils import date_utils
from models import *


class OriginatedAchTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, description: str, counterparty: Counterparty, tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'originatedAchTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.description = description
        self.counterparty = counterparty
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return OriginatedAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"],attributes["balance"],attributes["summary"], attributes["description"],
            Counterparty.from_json_api(attributes["counterparty"]), attributes.get("tags"), relationships)


class ReceivedAchTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, description: str, addenda: Optional[str], company_name: str,
                 counterparty_routing_number: str, trace_number: Optional[str], sec_code: Optional[str],
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'receivedAchTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.description = description
        self.addenda = addenda
        self.company_name = company_name
        self.counterparty_routing_number = counterparty_routing_number
        self.trace_number = trace_number
        self.sec_code = sec_code
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReceivedAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["description"],
            attributes.get("addenda"), attributes["companyName"], attributes["counterpartyRoutingNumber"],
            attributes.get("traceNumber"), attributes.get("secCode"), attributes.get("tags"), relationships)


class ReturnedAchTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, company_name: str, counterparty_name: str, counterparty_routing_number: str, reason: str,
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'returnedAchTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.description = description
        self.addenda = addenda
        self.company_name = company_name
        self.counterparty_routing_number = counterparty_routing_number
        self.reason = reason
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReturnedAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["companyName"],
            attributes["counterpartyName"], attributes["counterpartyRoutingNumber"], attributes["reason"],
            attributes.get("tags"), relationships)


class ReturnedReceivedAchTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 company_name: str, reason: str, tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'returnedReceivedAchTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.company_name = company_name
        self.reason = reason
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReturnedReceivedAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["companyName"],
            attributes["reason"], attributes.get("tags"), relationships)


class DishonoredAchTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 company_name: str, counterparty_routing_number: str, trace_number: str, reason: str,
                 sec_code: Optional[str], tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'dishonoredAchTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.description = description
        self.company_name = company_name
        self.counterparty_routing_number = counterparty_routing_number
        self.trace_number = trace_number
        self.reason = reason
        self.sec_code = sec_code
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DishonoredAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["companyName"],
            attributes["counterpartyRoutingNumber"], attributes["traceNumber"], attributes["reason"],
            attributes.get("secCode"), attributes.get("tags"), relationships)


class BookTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, description: str, addenda: Optional[str], counterparty: Counterparty,
                 relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'bookTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.counterparty = counterparty
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BookTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"],
            Counterparty.from_json_api(attributes["counterparty"]), relationships)


class PurchaseTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, card_last_4_digits: str, merchant: Merchant, coordinates: Coordinates, recurring: bool,
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'purchaseTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.card_last_4_digits = card_last_4_digits
        self.merchant = merchant
        self.coordinates = coordinates
        self.recurring = recurring
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PurchaseTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["cardLast4Digits"],
            Merchant.from_json_api(attributes["merchant"]), Coordinates.from_json_api(attributes["coordinates"]),
            attributes["recurring"], attributes.get("tags"), relationships)


class AtmTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, card_last_4_digits: str, atm_name: str, atm_location: Optional[str], surcharge: int,
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'atmTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.card_last_4_digits = card_last_4_digits
        self.atm_name = atm_name
        self.atm_location = atm_location
        self.surcharge = recurring
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AtmTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["cardLast4Digits"],
            attributes["atmName"], attributes.get("atmLocation"), attributes["surcharge"], attributes.get("tags"),
                                 relationships)


class FeeTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'feeTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return FeeTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                 attributes["amount"], attributes["balance"], attributes["summary"],
                                 attributes.get("tags"), relationships)


class CardTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, card_last_4_digits: int, tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'cardTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.card_last_4_digits = card_last_4_digits
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                  attributes["amount"], attributes["balance"], attributes["summary"],
                                  attributes["cardLast4Digits"], attributes.get("tags"), relationships)


class CardReversalTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, card_last_4_digits: int, tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'cardReversalTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.card_last_4_digits = card_last_4_digits
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardReversalTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["cardLast4Digits"],
                                 attributes.get("tags"), relationships)


class WireTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, counterparty: Counterparty, description: str, sender_reference: str,
                 reference_for_beneficiary: str, tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'wireTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.counterparty = counterparty
        self.description = description
        self.sender_reference = sender_reference
        self.reference_for_beneficiary = reference_for_beneficiary
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return WireTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"],
            Counterparty.from_json_api(attributes["counterparty"]), attributes["description"],
            attributes["senderReference"], attributes["referenceForBeneficiary"], attributes.get("tags"), relationships)


class ReleaseTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, sender_name: str, sender_address: str, sender_account_number: str,
                 counterparty: Counterparty, amount: int, direction: str, description: str, balance: int, summary: str,
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'releaseTransaction'
        self.created_at = created_at
        self.sender_name = sender_name
        self.sender_address = sender_address
        self.sender_account_number = sender_account_number
        self.counterparty = counterparty
        self.amount = amount
        self.direction = direction
        self.description = description
        self.balance = balance
        self.summary = summary
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReleaseTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["senderName"],
                                  attributes["senderAddress"], attributes["senderAccountNumber"], attributes["counterparty"],
                                  attributes["amount"], attributes["direction"], attributes["description"],
                                  attributes["balance"], attributes["summary"], attributes.get("tags"), relationships)


class AdjustmentTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 description: str, tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'adjustmentTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.description = description
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AdjustmentTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                  attributes["amount"], attributes["balance"],
                                  attributes["summary"], attributes["description"], attributes.get("tags"), relationships)


class InterestTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
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


class DisputeTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, dispute_id: str,
                 summary: str, reason: str, tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
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


class CheckDepositTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'checkDepositTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                          attributes["amount"], attributes["balance"], attributes["summary"],
                                          attributes.get("tags"), relationships)


class ReturnedCheckDepositTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 reason: str, tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = 'returnedCheckDepositTransaction'
        self.created_at = created_at
        self.direction = direction
        self.amount = amount
        self.balance = balance
        self.summary = summary
        self.reason = reason
        self.tags = tags
        self.relationships = relationships

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

class PatchTransactionRequest(object):
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

