from unit.utils import date_utils
from unit.models import *


def to_object_dict(d: Dict[str, object]):
    dict_to_return = {}

    for k in d.keys():
        v = None
        if k == "phone":
            v = Phone.from_json_api(d[k])
        elif k == "address":
            v = Address.from_json_api(d[k])
        elif k == "authorizedUsers":
            AuthorizedUser.from_json_api(d[k])
        elif k == "fullName":
            v = FullName.from_json_api(d[k])
        else:
            v = d[k]

        dict_to_return.update(k, v)

    return dict_to_return

#
# def map_to(_id, _type, attributes, relationships):
#     if _type == "account.closed":
#         return AccountClosedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "account.frozen":
#         return AccountFrozenEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "application.awaitingDocuments":
#         return ApplicationAwaitingDocumentsEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "application.denied":
#         return ApplicationDeniedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "application.pendingReview":
#         return ApplicationPendingReviewEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "card.activated":
#         return CardActivatedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "card.statusChanged":
#         return CardStatusChangedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "authorization.created":
#         return AuthorizationCreatedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "authorizationRequest.declined":
#         return AuthorizationRequestDeclinedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "authorizationRequest.pending":
#         return AuthorizationRequestPendingEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "authorizationRequest.approved":
#         return AuthorizationRequestApprovedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "document.approved":
#         return DocumentApprovedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "document.rejected":
#         return DocumentRejectedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "document.approved":
#         return DocumentApprovedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "checkDeposit.created":
#         return CheckDepositCreatedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "checkDeposit.clearing":
#         return CheckDepositClearingEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "checkDeposit.sent":
#         return CheckDepositSentEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "payment.clearing":
#         return PaymentClearingEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "payment.sent":
#         return PaymentSentEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "payment.returned":
#         return PaymentReturnedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "statements.created":
#         return StatementsCreatedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "transaction.created":
#         return TransactionCreatedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "customer.created":
#         return CustomerCreatedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     if _type == "account.reopened":
#         return AccountReopenedEvent.from_json_api(_id, _type, attributes, relationships)
#
#     return RawUnitObject(_id, _type, attributes, relationships)

class BaseEvent(object):
    def __init__(self, _id: str, _type: str, created_at: datetime, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = _id
        self.type = _type
        self.attributes = {"createdAt": created_at, "tags": tags}
        self.relationships = relationships


class AccountClosedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, close_reason: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["closeReason"] = close_reason

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountClosedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                  attributes["closeReason"], attributes.get("tags"), relationships)


class AccountFrozenEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, freeze_reason: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.type = 'account.frozen'
        self.attributes["freezeReason"] = freeze_reason

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountFrozenEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes["freezeReason"],
                                  attributes.get("tags"), relationships)


class ApplicationDeniedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationDeniedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                                      relationships)


class ApplicationPendingReviewEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationPendingReviewEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                             attributes.get("tags"), relationships)


class ApplicationAwaitingDocumentsEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationAwaitingDocumentsEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                                 attributes.get("tags"), relationships)


class AuthorizationCreatedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, card_last_4_digits: str, recurring: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["cardLast4Digits"] = card_last_4_digits
        self.attributes["recurring"] = recurring

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationCreatedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                         attributes["cardLast4Digits"], attributes["recurring"],
                                         attributes.get("tags"), relationships)


class AuthorizationCanceledEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, amount: int, available: int, card_last_4_digits: str,
                 recurring: bool, tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["amount"] = amount
        self.attributes["available"] = available
        self.attributes["cardLast4Digits"] = card_last_4_digits
        self.attributes["recurring"] = recurring

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationCanceledEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                          attributes["amount"], attributes["available"], attributes["cardLast4Digits"],
                                          attributes["recurring"], attributes.get("tags"), relationships)


class AuthorizationAmountChangedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, old_amount: int, new_amount: int, available: int,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["oldAmount"] = old_amount
        self.attributes["newAmount"] = new_amount
        self.attributes["available"] = available

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationAmountChangedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                                attributes["oldAmount"], attributes["newAmount"],
                                                attributes.get("tags"), relationships)


class AuthorizationDeclinedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, amount: int, available: int, card_last_4_digits: str,
                 merchant: Merchant, recurring: bool, reason: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["amount"] = amount
        self.attributes["available"] = available
        self.attributes["cardLast4Digits"] = card_last_4_digits
        self.attributes["merchant"] = merchant
        self.attributes["recurring"] = recurring
        self.attributes["reason"] = reason


    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationDeclinedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                          attributes["amount"], attributes["available"], attributes["cardLast4Digits"],
                                          Merchant.from_json_api(attributes["merchant"]), attributes["recurring"],
                                          attributes["reason"], attributes.get("tags"), relationships)


class AuthorizationRequestApprovedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, amount: str, status: str, approved_amount: str,
                 partial_approval_allowed: str, merchant: Dict[str, str], recurring: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["amount"] = amount
        self.attributes["status"] = status
        self.attributes["approvedAmount"] = approved_amount
        self.attributes["partialApprovalAllowed"] = partial_approval_allowed
        self.attributes["merchant"] = merchant
        self.attributes["recurring"] = recurring

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationRequestApprovedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                                 attributes["amount"], attributes["status"],
                                                 attributes["approvedAmount"], attributes["partialApprovalAllowed"],
                                                 attributes["merchant"], attributes["recurring"],
                                                 attributes.get("tags"), relationships)


class AuthorizationRequestDeclinedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, amount: str, status: str, decline_reason: str,
                 partial_approval_allowed: str, merchant: Dict[str, str], recurring: bool,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["amount"] = amount
        self.attributes["status"] = status
        self.attributes["declineReason"] = decline_reason
        self.attributes["partialApprovalAllowed"] = partial_approval_allowed
        self.attributes["merchant"] = merchant
        self.attributes["recurring"] = recurring

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationRequestDeclinedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                                 attributes["amount"], attributes["status"],
                                                 attributes["declineReason"], attributes["partialApprovalAllowed"],
                                                 attributes["merchant"], attributes["recurring"],
                                                 attributes.get("tags"), relationships)


class AuthorizationRequestPendingEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, attributes: Dict[str, object],
                 relationships: Optional[Dict[str, Relationship]]):

        BaseEvent.__init__(self, _id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                           relationships)
        self.attributes["amount"] = attributes["amount"]
        self.attributes["status"] = attributes["status"]
        self.attributes["partialApprovalAllowed"] = attributes["partialApprovalAllowed"]
        self.attributes["merchant"] = attributes["merchant"]
        self.attributes["recurring"] = attributes["recurring"]
        self.attributes["direction"] = attributes.get("direction")
        self.attributes["available"] = attributes.get("available")
        self.attributes["ecommerce"] = attributes.get("ecommerce")
        self.attributes["cardPresent"] = attributes.get("cardPresent")
        self.attributes["healthcareAmounts"] = HealthcareAmounts.from_json_api(attributes.get("healthcareAmounts"))

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationRequestPendingEvent(_id, _type, attributes, relationships)


class CardActivatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardActivatedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                                  relationships)


class CardStatusChangedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, attributes: Dict[str, object],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                           relationships)
        self.attributes["newStatus"] = attributes["newStatus"]
        self.attributes["previousStatus"] = attributes["previousStatus"]

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardStatusChangedEvent(_id, _type, attributes, relationships)


class CardCreatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardCreatedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                                  relationships)


class CheckDepositCreatedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["status"] = status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositCreatedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                        attributes["status"], attributes.get("tags"), relationships)


class CheckDepositClearingEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositClearingEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                         attributes["previousStatus"], attributes.get("tags"), relationships)


class CheckDepositSentEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositSentEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                     attributes["previousStatus"], attributes.get("tags"), relationships)


class CheckDepositReturnedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositReturnedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                         attributes["previousStatus"], attributes.get("tags"), relationships)


class CheckDepositPendingReviewEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositPendingReviewEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                              attributes["previousStatus"], attributes.get("tags"), relationships)


class CheckDepositPendingEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositPendingEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                        attributes["previousStatus"], attributes.get("tags"), relationships)


class CustomerArchivedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, attributes: Dict[str, object],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                           relationships)
        self.attributes["previousStatus"] = attributes["previousStatus"]
        self.attributes["archiveReason"] = attributes["archiveReason"]

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CustomerArchivedEvent(_id, _type, attributes, relationships)


class CustomerCreatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CustomerCreatedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                    attributes.get("tags"), relationships)


class CustomerUpdatedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, attributes: Dict[str, object],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                           relationships)
        self.attributes["changes"] = to_object_dict(attributes["changes"])

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CustomerUpdatedEvent(_id, _type, attributes, relationships)


class DocumentApprovedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DocumentApprovedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                     attributes.get("tags"), relationships)


class DocumentRejectedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, reason: str, reason_code: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["reason"] = reason
        self.attributes["reasonCode"] = reason_code

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DocumentRejectedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                     attributes["reason"], attributes["reasonCode"], attributes.get("tags"),
                                     relationships)


class PaymentClearingEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentClearingEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes["previousStatus"],
                                    attributes.get("tags"), relationships)


class PaymentSentEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentSentEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                attributes["previousStatus"], attributes.get("tags"), relationships)


class PaymentReturnedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentReturnedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes["previousStatus"],
                                    attributes.get("tags"), relationships)


class StatementsCreatedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, period: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["period"] = period

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return StatementsCreatedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes["period"],
                                    attributes.get("tags"), relationships)


class TransactionCreatedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, created_at: datetime, summary: str, direction: str, amount: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, created_at, tags, relationships)
        self.attributes["summary"] = summary
        self.attributes["direction"] = direction
        self.attributes["amount"] = amount

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return TransactionCreatedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                       attributes["summary"], attributes["direction"], attributes["amount"],
                                       attributes.get("tags"), relationships)


class AccountReopenedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountReopenedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                                    relationships)


class AccountCreatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountCreatedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                                   relationships)


class AccountUnFrozenEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountUnFrozenEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                                    relationships)


class ApplicationCreated(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationCreated(_id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                                  relationships)


class ApplicationCreatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationCreated(_id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                                  relationships)


class ApplicationCanceledEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ApplicationCanceledEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                        attributes.get("tags"), relationships)


class BulkPaymentsFailedEvent(BaseEvent):
    def __init__(self, _id: str, _type: str, attributes: Dict[str, object],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, _id, _type, date_utils.to_datetime(attributes["createdAt"]), attributes.get("tags"),
                           relationships)
        self.attributes["index"] = attributes["index"]
        self.attributes["error"] = attributes["error"]
        self.attributes["idempotencyKey"] = attributes["idempotencyKey"]

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BulkPaymentsFailedEvent(_id, _type, attributes, relationships)


class BulkPaymentsFinishedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BulkPaymentsFinishedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                         attributes.get("tags"), relationships)


class DeclinedIncomingPaymentCreatedEvent(BaseEvent):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DeclinedIncomingPaymentCreatedEvent(_id, _type, date_utils.to_datetime(attributes["createdAt"]),
                                         attributes.get("tags"), relationships)


EventDTO = Union[AccountClosedEvent, AccountFrozenEvent, ApplicationDeniedEvent, ApplicationAwaitingDocumentsEvent,
                 ApplicationPendingReviewEvent, CardActivatedEvent, CardStatusChangedEvent, CardCreatedEvent,
                 AuthorizationCreatedEvent, AuthorizationRequestDeclinedEvent, AuthorizationRequestPendingEvent,
                 AuthorizationRequestApprovedEvent, DocumentApprovedEvent, DocumentRejectedEvent,
                 CheckDepositCreatedEvent, CheckDepositClearingEvent, CheckDepositSentEvent,
                 CheckDepositReturnedEvent, CheckDepositPendingEvent, CheckDepositPendingReviewEvent,
                 CustomerCreatedEvent, CustomerUpdatedEvent, CustomerArchivedEvent, PaymentClearingEvent,
                 PaymentSentEvent, PaymentReturnedEvent, StatementsCreatedEvent, TransactionCreatedEvent,
                 AccountReopenedEvent, AccountCreatedEvent, AccountUnFrozenEvent, ApplicationCreatedEvent,
                 ApplicationCanceledEvent, AuthorizationCanceledEvent, AuthorizationAmountChangedEvent,
                 AuthorizationDeclinedEvent, BulkPaymentsFailedEvent, BulkPaymentsFinishedEvent,
                 DeclinedIncomingPaymentCreatedEvent, RawUnitObject]


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
