import json
from datetime import datetime, date
from typing import Literal, Optional
from unit.utils import date_utils
from unit.models import *

class BaseEvent(object):
    def __init__(self, id: str, created_at: datetime, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.attributes = {"createdAt": created_at, "tags": tags}
        self.relationships = relationships


class AccountClosedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, close_reason: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'account.closed'
        self.attributes["closeReason"] = close_reason

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountClosedEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["closeReason"],
                                  attributes.get("tags"), relationships)


class AccountFrozenEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, freeze_reason: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'account.frozen'
        self.attributes["freezeReason"] = freeze_reason

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountFrozenEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["freezeReason"],
                                  attributes.get("tags"), relationships)


class ApplicationDeniedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'application.denied'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationDeniedEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                                      relationships)


class ApplicationPendingReviewEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'application.pendingReview'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationPendingReviewEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                             attributes.get("tags"), relationships)


class ApplicationAwaitingDocumentsEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'application.awaitingDocuments'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationAwaitingDocumentsEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                                 attributes.get("tags"), relationships)


class AuthorizationCreatedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, card_last_4_digits: str, recurring: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'authorization.created'
        self.attributes["cardLast4Digits"] = card_last_4_digits
        self.attributes["recurring"] = recurring

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationCreatedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                         attributes["cardLast4Digits"], attributes["recurring"],
                                         attributes.get("tags"), relationships)

class AuthorizationRequestApprovedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, amount: str, status: str, approved_amount: str,
                 partial_approval_allowed: str, merchant: Dict[str, str], recurring: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'authorizationRequest.approved'
        self.attributes["amount"] = amount
        self.attributes["status"] = status
        self.attributes["approvedAmount"] = approved_amount
        self.attributes["partialApprovalAllowed"] = partial_approval_allowed
        self.attributes["merchant"] = merchant
        self.attributes["recurring"] = recurring


    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationRequestApprovedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                                 attributes["amount"], attributes["status"],
                                                 attributes["approvedAmount"], attributes["partialApprovalAllowed"],
                                                 attributes["merchant"], attributes["recurring"],
                                                 attributes.get("tags"), relationships)


class AuthorizationRequestDeclinedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, amount: str, status: str, decline_reason: str,
                 partial_approval_allowed: str, merchant: Dict[str, str], recurring: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'authorizationRequest.declined'
        self.attributes["amount"] = amount
        self.attributes["status"] = status
        self.attributes["declineReason"] = decline_reason
        self.attributes["partialApprovalAllowed"] = partial_approval_allowed
        self.attributes["merchant"] = merchant
        self.attributes["recurring"] = recurring


    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationRequestDeclinedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                                 attributes["amount"], attributes["status"],
                                                 attributes["declineReason"], attributes["partialApprovalAllowed"],
                                                 attributes["merchant"], attributes["recurring"],
                                                 attributes.get("tags"), relationships)


class AuthorizationRequestPendingEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, amount: str, status: str, partial_approval_allowed: str,
                 merchant: Dict[str, str], recurring: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'authorizationRequest.pending'
        self.attributes["amount"] = amount
        self.attributes["status"] = status
        self.attributes["partialApprovalAllowed"] = partial_approval_allowed
        self.attributes["merchant"] = merchant
        self.attributes["recurring"] = recurring


    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationRequestPendingEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                                attributes["amount"], attributes["status"],
                                                attributes["partialApprovalAllowed"], attributes["merchant"],
                                                attributes["recurring"], attributes.get("tags"), relationships)

class CardActivatedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'card.activated'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardActivatedEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                                  relationships)


class CardStatusChangedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, new_status: str, previous_status: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'card.statusChanged'
        self.attributes["newStatus"] = new_status
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardStatusChangedEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["newStatus"],
                                      attributes["previousStatus"], attributes.get("tags"), relationships)


class CheckDepositCreatedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkDeposit.created'
        self.attributes["status"] = status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositCreatedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                      attributes["status"], attributes.get("tags"), relationships)

class CheckDepositClearingEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkDeposit.clearing'
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositClearingEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                      attributes["previousStatus"], attributes.get("tags"), relationships)


class CheckDepositSentEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkDeposit.sent'
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositSentEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                      attributes["previousStatus"], attributes.get("tags"), relationships)


class CheckDepositReturnedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkDeposit.returned'
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositReturnedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                      attributes["previousStatus"], attributes.get("tags"), relationships)


class CustomerCreatedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'customer.created'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CustomerCreatedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                    attributes.get("tags"), relationships)

class DocumentApprovedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'document.approved'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DocumentApprovedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                    attributes.get("tags"), relationships)

class DocumentRejectedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, reason: str, reason_code: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'document.rejected'
        self.attributes["reason"] = reason
        self.attributes["reasonCode"] = reason_code

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DocumentRejectedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                     attributes["reason"], attributes["reasonCode"], attributes.get("tags"),
                                     relationships)


class PaymentClearingEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'payment.clearing'
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentClearingEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["previousStatus"],
                                    attributes.get("tags"), relationships)

class PaymentSentEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'payment.sent'
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentSentEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["previousStatus"],
                                    attributes.get("tags"), relationships)

class PaymentReturnedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'payment.returned'
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentReturnedEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["previousStatus"],
                                    attributes.get("tags"), relationships)

class StatementsCreatedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, period: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'statements.created'
        self.attributes["period"] = period

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return StatementsCreatedEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["period"],
                                    attributes.get("tags"), relationships)

class TransactionCreatedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, summary: str, direction: str, amount: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'transaction.created'
        self.attributes["summary"] = summary
        self.attributes["direction"] = direction
        self.attributes["amount"] = amount

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return TransactionCreatedEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["summary"],
                                       attributes["direction"], attributes["amount"], attributes.get("tags"),
                                       relationships)

class AccountReopenedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime,tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'account.reopened'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountReopenedEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                                    relationships)

EventDTO = Union[AccountClosedEvent, AccountFrozenEvent, ApplicationDeniedEvent, ApplicationAwaitingDocumentsEvent,
                 ApplicationPendingReviewEvent, CardActivatedEvent, CardStatusChangedEvent,
                 AuthorizationCreatedEvent, AuthorizationRequestDeclinedEvent, AuthorizationRequestPendingEvent,
                 AuthorizationRequestApprovedEvent, DocumentApprovedEvent, DocumentRejectedEvent,
                 CheckDepositCreatedEvent, CheckDepositClearingEvent, CheckDepositSentEvent,
                 CheckDepositReturnedEvent, CustomerCreatedEvent, PaymentClearingEvent, PaymentSentEvent,
                 PaymentReturnedEvent, StatementsCreatedEvent, TransactionCreatedEvent, AccountReopenedEvent, RawUnitObject]


class ListEventParams(UnitParams):
    def __init__(self, limit: int = 100, offset: int = 0, type: Optional[List[str]] = None):
        self.limit = limit
        self.offset = offset
        self.type = type

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.type:
            parameters["filter[type][]"] = self.type
        return parameters
