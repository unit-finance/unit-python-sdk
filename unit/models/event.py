from unit.utils import to_relationships

try:
    from typing import Literal, Optional
except ImportError:
    from typing import Optional
    from typing_extensions import Literal
from unit.utils import date_utils
from unit.models import *


class BaseEvent(object):
    def __init__(self, _id: str, _type: str, attributes: Dict[str, object], relationships: Dict[str, Relationship]):
        self.id = _id
        self.type = _type
        self.attributes = self.__to_attributes(attributes)
        self.relationships = relationships

    @staticmethod
    def __to_attributes(data: Dict[str, object]):
        if "createdAt" in data.keys():
            data["createdAt"] = date_utils.to_datetime(data["createdAt"])

        return data


class AccountClosedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountClosedEvent(_id, _type, attributes, relationships)


class AccountFrozenEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountFrozenEvent(_id, _type, attributes, relationships)


class ApplicationDeniedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationDeniedEvent(_id, _type, attributes, relationships)


class ApplicationPendingReviewEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationPendingReviewEvent(_id, _type, attributes, relationships)


class ApplicationAwaitingDocumentsEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationAwaitingDocumentsEvent(_id, _type, attributes, relationships)


class AuthorizationCreatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationCreatedEvent(_id, _type, attributes, relationships)


class AuthorizationRequestApprovedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationRequestApprovedEvent(_id, _type, attributes, relationships)


class AuthorizationRequestDeclinedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationRequestDeclinedEvent(_id, _type, attributes, relationships)


class AuthorizationRequestPendingEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationRequestPendingEvent(_id, _type, attributes, relationships)


class CardActivatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardActivatedEvent(_id, _type, attributes, relationships)


class CardStatusChangedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardStatusChangedEvent(_id, _type, attributes, relationships)


class CheckDepositCreatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositCreatedEvent(_id, _type, attributes, relationships)


class CheckDepositClearingEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositClearingEvent(_id, _type, attributes, relationships)


class CheckDepositSentEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositSentEvent(_id, _type, attributes, relationships)


class CheckDepositReturnedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositReturnedEvent(_id, _type, attributes, relationships)


class CustomerCreatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CustomerCreatedEvent(_id, _type, attributes, relationships)


class DocumentApprovedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DocumentApprovedEvent(_id, _type, attributes, relationships)


class DocumentRejectedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DocumentRejectedEvent(_id, _type, attributes, relationships)


class PaymentClearingEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentClearingEvent(_id, _type, attributes, relationships)


class PaymentSentEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentSentEvent(_id, _type, attributes, relationships)


class PaymentReturnedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentReturnedEvent(_id, _type, attributes, relationships)


class StatementsCreatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return StatementsCreatedEvent(_id, _type, attributes, relationships)


class TransactionCreatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return TransactionCreatedEvent(_id, _type, attributes, relationships)


class AccountReopenedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountReopenedEvent(_id, _type, attributes, relationships)


class CheckPaymentCreatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentCreatedEvent(_id, _type, attributes, relationships)


class CheckPaymentMarkedForReturnEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentMarkedForReturnEvent(_id, _type, attributes, relationships)


class CheckPaymentProcessedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentProcessedEvent(_id, _type, attributes, relationships)


class CheckPaymentReturnedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentReturnedEvent(_id, _type, attributes, relationships)


class CheckPaymentPendingEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentPendingEvent(_id, _type, attributes, relationships)

class CheckPaymentProcessedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentProcessedEvent(_id, _type, attributes, relationships)


class CheckPaymentReturnedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentReturnedEvent(_id, _type, attributes, relationships)


class CheckPaymentPendingEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentPendingEvent(_id, _type, attributes, relationships)


EventDTO = Union[AccountClosedEvent, AccountFrozenEvent, ApplicationDeniedEvent, ApplicationPendingReviewEvent,
                 ApplicationAwaitingDocumentsEvent, AuthorizationCreatedEvent, AuthorizationRequestApprovedEvent,
                 AuthorizationRequestDeclinedEvent, AuthorizationRequestPendingEvent, CardActivatedEvent,
                 CardStatusChangedEvent, CheckDepositCreatedEvent, CheckDepositClearingEvent, CheckDepositSentEvent,
                 CheckDepositReturnedEvent, CustomerCreatedEvent, DocumentApprovedEvent, DocumentRejectedEvent,
                 PaymentClearingEvent, PaymentSentEvent, PaymentReturnedEvent, StatementsCreatedEvent,
                 TransactionCreatedEvent, AccountReopenedEvent, CheckPaymentCreatedEvent,
                 CheckPaymentMarkedForReturnEvent, CheckPaymentProcessedEvent, CheckPaymentReturnedEvent,
                 CheckPaymentPendingEvent]


def events_mapper(_id, _type, attributes, relationships):
    c = globals()
    dot = _type.index(".")
    c_name = _type[0].upper() + _type[1:dot] + _type[dot+1].upper() + _type[dot+2:] + "Event"
    if c_name in c.keys():
        return c[c_name].from_json_api(_id, _type, attributes, relationships)
    else:
        return RawUnitObject(_id, _type, attributes, relationships)

class TaxFormCreatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return TaxFormCreatedEvent(_id, _type, attributes, relationships)


class TaxFormUpdatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return TaxFormUpdatedEvent(_id, _type, attributes, relationships)


EventDTO = Union[AccountClosedEvent, AccountFrozenEvent, ApplicationDeniedEvent, ApplicationPendingReviewEvent,
                 ApplicationAwaitingDocumentsEvent, AuthorizationCreatedEvent, AuthorizationRequestApprovedEvent,
                 AuthorizationRequestDeclinedEvent, AuthorizationRequestPendingEvent, CardActivatedEvent,
                 CardStatusChangedEvent, CheckDepositCreatedEvent, CheckDepositClearingEvent, CheckDepositSentEvent,
                 CheckDepositReturnedEvent, CustomerCreatedEvent, DocumentApprovedEvent, DocumentRejectedEvent,
                 PaymentClearingEvent, PaymentSentEvent, PaymentReturnedEvent, StatementsCreatedEvent,
                 TransactionCreatedEvent, AccountReopenedEvent, CheckPaymentCreatedEvent,
                 CheckPaymentMarkedForReturnEvent, CheckPaymentProcessedEvent, CheckPaymentReturnedEvent,
                 CheckPaymentPendingEvent, TaxFormCreatedEvent, TaxFormUpdatedEvent]


def events_mapper(_id, _type, attributes, relationships):
    c = globals()
    dot = _type.index(".")
    c_name = _type[0].upper() + _type[1:dot] + _type[dot+1].upper() + _type[dot+2:] + "Event"
    if c_name in c.keys():
        return c[c_name].from_json_api(_id, _type, attributes, relationships)
    else:
        return RawUnitObject(_id, _type, attributes, relationships)


class ListEventParams(UnitParams):
    def __init__(self, limit: int = 100, offset: int = 0, type: Optional[List[str]] = None, since: Optional[str] = None,
                 until: Optional[str] = None):
        self.limit = limit
        self.offset = offset
        self.type = type
        self.since = since
        self.until = until

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.type:
            parameters["filter[type][]"] = self.type
        if self.since:
            parameters["filter[since]"] = self.since
        if self.until:
            parameters["filter[until]"] = self.until
        return parameters
