from unit.models import *


class AccountClosedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountClosedEvent(_id, _type, attributes_to_object(attributes), relationships)


class AccountFrozenEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountFrozenEvent(_id, _type, attributes_to_object(attributes), relationships)


class ApplicationDeniedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationDeniedEvent(_id, _type, attributes_to_object(attributes), relationships)


class ApplicationPendingReviewEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationPendingReviewEvent(_id, _type, attributes_to_object(attributes), relationships)


class ApplicationAwaitingDocumentsEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationAwaitingDocumentsEvent(_id, _type, attributes_to_object(attributes), relationships)


class AuthorizationCreatedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationCreatedEvent(_id, _type, attributes_to_object(attributes), relationships)


class AuthorizationRequestApprovedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationRequestApprovedEvent(_id, _type, attributes_to_object(attributes), relationships)


class AuthorizationRequestDeclinedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationRequestDeclinedEvent(_id, _type, attributes_to_object(attributes), relationships)


class AuthorizationRequestPendingEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationRequestPendingEvent(_id, _type, attributes_to_object(attributes), relationships)


class CardActivatedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardActivatedEvent(_id, _type, attributes_to_object(attributes), relationships)


class CardStatusChangedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardStatusChangedEvent(_id, _type, attributes_to_object(attributes), relationships)


class CheckDepositCreatedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositCreatedEvent(_id, _type, attributes_to_object(attributes), relationships)


class CheckDepositClearingEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositClearingEvent(_id, _type, attributes_to_object(attributes), relationships)


class CheckDepositSentEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositSentEvent(_id, _type, attributes_to_object(attributes), relationships)


class CheckDepositReturnedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositReturnedEvent(_id, _type, attributes_to_object(attributes), relationships)


class CustomerCreatedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CustomerCreatedEvent(_id, _type, attributes_to_object(attributes), relationships)


class DocumentApprovedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DocumentApprovedEvent(_id, _type, attributes_to_object(attributes), relationships)


class DocumentRejectedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DocumentRejectedEvent(_id, _type, attributes_to_object(attributes), relationships)


class PaymentClearingEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentClearingEvent(_id, _type, attributes_to_object(attributes), relationships)


class PaymentSentEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentSentEvent(_id, _type, attributes_to_object(attributes), relationships)


class PaymentReturnedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentReturnedEvent(_id, _type, attributes_to_object(attributes), relationships)


class StatementsCreatedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return StatementsCreatedEvent(_id, _type, attributes_to_object(attributes), relationships)


class TransactionCreatedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return TransactionCreatedEvent(_id, _type, attributes_to_object(attributes), relationships)


class AccountReopenedEvent(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountReopenedEvent(_id, _type, attributes_to_object(attributes), relationships)


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
