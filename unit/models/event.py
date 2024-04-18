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

class AuthorizationCanceledEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, amount: int, card_last_4_digits: str,
                 recurring: str, tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'authorization.canceled'
        self.attributes["cardLast4Digits"] = card_last_4_digits
        self.attributes["amount"] = amount
        self.attributes["recurring"] = recurring

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationCanceledEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                          attributes["amount"], attributes["cardLast4Digits"],
                                          attributes["recurring"], attributes.get("tags"),
                                          relationships)

class AuthorizationDeclinedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, amount: int, card_last_4_digits: str, merchant: Merchant,
                 reason: str, recurring: str, tags: Optional[Dict[str, str]] = None,
                 relationships: Optional[Dict[str, Relationship]] = None):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'authorization.declined'
        self.attributes["cardLast4Digits"] = card_last_4_digits
        self.attributes["amount"] = amount
        self.attributes["reason"] = reason
        self.attributes["merchant"] = merchant
        self.attributes["recurring"] = recurring

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationDeclinedEvent(
            id=_id, created_at=date_utils.to_datetime(attributes["createdAt"]),
            amount=attributes["amount"], card_last_4_digits=attributes["cardLast4Digits"],
            merchant=Merchant.from_json_api(attributes["merchant"]), reason=attributes.get("reason"), recurring=attributes["recurring"],
            tags=attributes.get("tags"), relationships=relationships)

class AuthorizationCreatedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, amount: int, card_last_4_digits: str, merchant: Merchant,
                 recurring: str, tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'authorization.created'
        self.attributes["cardLast4Digits"] = card_last_4_digits
        self.attributes["amount"] = amount
        self.attributes["merchant"] = merchant
        self.attributes["recurring"] = recurring

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationCreatedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                         attributes["amount"], attributes["cardLast4Digits"], Merchant.from_json_api(attributes["merchant"]),
                                         attributes["recurring"], attributes.get("tags"), relationships)

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
    def __init__(self, id: str, created_at: datetime, amount: int, status: str, partial_approval_allowed: str,
                 card_present: bool, digital_wallet: str, ecommerce: bool, merchant: Merchant, recurring: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'authorizationRequest.pending'
        self.attributes["amount"] = amount
        self.attributes["status"] = status
        self.attributes["cardPresent"] = card_present
        self.attributes["digitalWallet"] = digital_wallet
        self.attributes["ecommerce"] = ecommerce
        self.attributes["partialApprovalAllowed"] = partial_approval_allowed
        self.attributes["merchant"] = merchant
        self.attributes["recurring"] = recurring


    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationRequestPendingEvent(
            id=_id,
            created_at=date_utils.to_datetime(attributes["createdAt"]),
            amount=attributes["amount"],
            status=attributes["status"],
            ecommerce=attributes.get("ecommerce"),
            card_present=attributes.get("cardPresent"),
            digital_wallet=attributes.get("digitalWallet"),
            partial_approval_allowed=attributes["partialApprovalAllowed"],
            merchant=Merchant.from_json_api(attributes["merchant"]),
            recurring=attributes["recurring"],
            tags=attributes.get("tags"),
            relationships=relationships
        )

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


class CheckDepositPendingReviewEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkDeposit.pendingReview'
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositCreatedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                      attributes["previousStatus"], attributes.get("tags"), relationships)


class CheckDepositPendingEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkDeposit.pending'
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositCreatedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                      attributes["previousStatus"], attributes.get("tags"), relationships)


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


class CheckDepositRejectedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, previous_status: str, reason: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkDeposit.rejected'
        self.attributes["previousStatus"] = previous_status
        self.attributes["reason"] = reason

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositRejectedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                      attributes["previousStatus"], attributes["reason"], attributes.get("tags"), relationships)



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


class CheckPaymentCreatedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, status: str, additional_verification_status: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkPayment.created'
        self.attributes["status"] = status
        self.attributes["additionalVerificationStatus"] = additional_verification_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentCreatedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                        attributes["status"], attributes["additionalVerificationStatus"],
                                        attributes.get("tags"), relationships)


class CheckPaymentMarkedForReturnEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkPayment.markedForReturn'
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentMarkedForReturnEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                                attributes["previousStatus"], attributes.get("tags"), relationships)


class CheckPaymentProcessedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, previous_status: str, additional_verification_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkPayment.processed'
        self.attributes["previousStatus"] = previous_status
        self.attributes["additionalVerificationStatus"] = additional_verification_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentProcessedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                          attributes["previousStatus"], attributes["additionalVerificationStatus"],
                                          attributes.get("tags"), relationships)


class CheckPaymentReturnedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkPayment.returned'
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentReturnedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                         attributes["previousStatus"], attributes.get("tags"), relationships)


class CheckPaymentPendingEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, status: str, previous_status: str,
                 counterparty_moved: Optional[bool], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkPayment.pending'
        self.attributes["status"] = status
        self.attributes["previousStatus"] = previous_status
        self.attributes["counterpartyMoved"] = counterparty_moved

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentPendingEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                        attributes["status"], attributes["previousStatus"],
                                        attributes.get("counterpartyMoved"), attributes.get("tags"), relationships)


class CheckPaymentRejectedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, status: str, previous_status: str,
                 reject_reason: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkPayment.rejected'
        self.attributes["status"] = status
        self.attributes["previousStatus"] = previous_status
        self.attributes["rejectReason"] = reject_reason

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentRejectedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                         attributes["status"], attributes["previousStatus"],
                                         attributes["rejectReason"], attributes.get("tags"), relationships)


class CheckPaymentInProductionEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, status: str, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkPayment.inProduction'
        self.attributes["status"] = status
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentInProductionEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                                             attributes["previousStatus"], attributes.get("tags"), relationships)


class CheckPaymentInDeliveryEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, status: str, previous_status: str, delivery_status: str,
                 tracked_at: datetime, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkPayment.inDelivery'
        self.attributes["status"] = status
        self.attributes["previousStatus"] = previous_status
        self.attributes["deliveryStatus"] = delivery_status
        self.attributes["trackedAt"] = tracked_at

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentInDeliveryEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                                           attributes["previousStatus"], attributes["deliveryStatus"],
                                           attributes["trackedAt"], attributes.get("tags"), relationships)


class CheckPaymentDeliveredEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, status: str, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkPayment.delivered'
        self.attributes["status"] = status
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentDeliveredEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                                          attributes["previousStatus"], attributes.get("tags"), relationships)


class CheckPaymentReturnToSenderEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, status: str, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkPayment.returnToSender'
        self.attributes["status"] = status
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentDeliveredEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                                          attributes["previousStatus"], attributes.get("tags"), relationships)


class CheckPaymentCanceledEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, previous_status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkPayment.canceled'
        self.attributes["previousStatus"] = previous_status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentCanceledEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                          attributes["previousStatus"], attributes.get("tags"), relationships)


class CheckPaymentDeliveryStatusChangedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, previous_delivery_status: str, new_delivery_status: str,
                 tracked_at: datetime, postal_code: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkPayment.deliveryStatusChanged'
        self.attributes["previousDeliveryStatus"] = previous_delivery_status
        self.attributes["NewDeliveryStatus"] = new_delivery_status
        self.attributes["trackedAt"] = tracked_at
        self.attributes["postalCode"] = postal_code

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentDeliveryStatusChangedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                                      attributes["previousDeliveryStatus"],
                                                      attributes["NewDeliveryStatus"], attributes["trackedAt"],
                                                      attributes["postalCode"], attributes.get("tags"), relationships)


class CheckPaymentAdditionalVerificationRequiredEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, status: str, amount: int, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkPayment.additionalVerificationRequired'
        self.attributes["status"] = status
        self.attributes["amount"] = amount

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentAdditionalVerificationRequiredEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                      attributes["status"], attributes["amount"], attributes.get("tags"), relationships)


class CheckPaymentAdditionalVerificationApprovedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, status: str, amount: int, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'checkPayment.additionalVerificationApproved'
        self.attributes["status"] = status
        self.attributes["amount"] = amount

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentAdditionalVerificationApprovedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                      attributes["status"], attributes["amount"], attributes.get("tags"), relationships)


class CustomerCreatedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'customer.created'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CustomerCreatedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
                                    attributes.get("tags"), relationships)


class CustomerUpdatedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'customer.updated'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CustomerUpdatedEvent(_id, date_utils.to_datetime(attributes["createdAt"]),
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

class PaymentCreatedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'payment.created'
        self.attributes["status"] = status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentCreatedEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                                    attributes.get("tags"), relationships)

class PaymentRejectedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, status: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'payment.rejected'
        self.attributes["status"] = status

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentClearingEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                                    attributes.get("tags"), relationships)

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

class PaymentRejectedEvent(BaseEvent):
    def __init__(self, id: str, created_at: datetime, reason: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseEvent.__init__(self, id, created_at, tags, relationships)
        self.type = 'payment.rejected'
        self.attributes["reason"] = reason

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentRejectedEvent(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["reason"],
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
    def __init__(self, id: str, created_at: datetime, summary: str, direction: str, amount: int,
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

EventDTO = Union[
    AccountClosedEvent, AccountFrozenEvent, ApplicationDeniedEvent, ApplicationAwaitingDocumentsEvent,
    ApplicationPendingReviewEvent, CardActivatedEvent, CardStatusChangedEvent,
    AuthorizationCreatedEvent, AuthorizationCanceledEvent, AuthorizationDeclinedEvent,
    AuthorizationRequestDeclinedEvent, AuthorizationRequestPendingEvent,
    AuthorizationRequestApprovedEvent, DocumentApprovedEvent, DocumentRejectedEvent,
    CheckDepositCreatedEvent, CheckDepositPendingReviewEvent, CheckDepositPendingEvent,
    CheckDepositClearingEvent, CheckDepositSentEvent, CheckDepositRejectedEvent, CheckDepositReturnedEvent,
    CheckPaymentCreatedEvent, CheckPaymentMarkedForReturnEvent, CheckPaymentProcessedEvent, CheckPaymentReturnedEvent,
    CheckPaymentPendingEvent, CheckPaymentRejectedEvent, CheckPaymentInProductionEvent, CheckPaymentInDeliveryEvent,
    CheckPaymentDeliveredEvent, CheckPaymentReturnToSenderEvent, CheckPaymentCanceledEvent,
    CheckPaymentDeliveryStatusChangedEvent, CheckPaymentAdditionalVerificationRequiredEvent,
    CheckPaymentAdditionalVerificationApprovedEvent,
    CustomerCreatedEvent, PaymentClearingEvent, PaymentSentEvent, PaymentReturnedEvent,
    StatementsCreatedEvent, TransactionCreatedEvent, AccountReopenedEvent, RawUnitObject,
]


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
