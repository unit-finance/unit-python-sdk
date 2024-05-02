import json
from typing import Optional, Literal
from unit.models import *
from unit.utils import date_utils


CheckPaymentStatus = Literal["New", "Pending", "PendingCancellation", "Canceled", "InDelivery", "Delivered",
    "ReturnedToSender", "Processed", "PendingReview", "MarkedForReturn", "Returned", "Rejected"]
CheckPaymentAdditionalVerificationStatus = Literal["Required", "NotRequired", "Approved"]
CheckPaymentReturnStatusReason = Literal[
    "NotSufficientFunds",
    "UncollectedFundsHold",
    "StopPayment",
    "ClosedAccount",
    "UnableToLocateAccount",
    "FrozenOrBlockedAccount",
    "StaleDated",
    "PostDated",
    "NotValidCheckOrCashItem",
    "AlteredOrFictitious",
    "UnableToProcess",
    "ItemExceedsDollarLimit",
    "NotAuthorized",
    "ReferToMaker",
    "UnusableImage",
    "DuplicatePresentment",
    "WarrantyBreach",
    "UnauthorizedWarrantyBreach"
]
CheckPaymentDeliveryStatus = Literal["Mailed", "InLocalArea", "Delivered", "Rerouted", "ReturnedToSender"]


class CheckPaymentDTO(object):
    def __init__(self, id: str, created_at: datetime, updated_at: datetime, amount: int, status: CheckPaymentStatus,
                 description: str, originated: bool, check_number: Optional[str], on_us: Optional[str],
                 on_us_auxiliary: Optional[str], counterparty_routing_number: Optional[str],
                 return_status_reason: Optional[CheckPaymentReturnStatusReason], reject_reason: Optional[str],
                 pending_review_reasons: Optional[List[str]], return_cutoff_time: Optional[datetime],
                 additional_verification_status: Optional[CheckPaymentAdditionalVerificationStatus],
                 tags: Optional[Dict[str, str]], delivery_status: Optional[CheckPaymentDeliveryStatus],
                 tracked_at: Optional[datetime], postal_code: Optional[str], expiration_date: Optional[date],
                 expected_delivery: Optional[date], send_at: Optional[datetime],
                 counterparty_name: Optional[str], counterparty_moved: Optional[bool],
                 counterparty_street: Optional[str],
                 counterparty_street2: Optional[str], counterparty_city: Optional[str],
                 counterparty_state: Optional[str],
                 counterparty_postal_code: Optional[str], counterparty_country: Optional[str], memo: Optional[str],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "checkPayment"
        self.attributes = self.attributes = {
            "createdAt": created_at,
            "updatedAt": updated_at,
            "amount": amount,
            "status": status,
            "description": description,
            "checkNumber": check_number,
            "originated": originated,
            "onUs": on_us,
            "onUsAuxiliary": on_us_auxiliary,
            "counterpartyRoutingNumber": counterparty_routing_number,
            "returnStatusReason": return_status_reason,
            "rejectReason": reject_reason,
            "pendingReviewReasons": pending_review_reasons,
            "returnCutoffTime": return_cutoff_time,
            "additionalVerificationStatus": additional_verification_status,
            "tags": tags,
            "deliveryStatus": delivery_status,
            "trackedAt": tracked_at,
            "postalCode": postal_code,
            "expirationDate": expiration_date,
            "expectedDelivery": expected_delivery,
            "sendAt": send_at,
            "counterparty": {
                "name": counterparty_name,
                "moved": counterparty_moved,
                "address": {
                    "street": counterparty_street,
                    "street2": counterparty_street2,
                    "city": counterparty_city,
                    "state": counterparty_state,
                    "postalCode": counterparty_postal_code,
                    "country": counterparty_country,
                }
            },
            "memo": memo,
        }
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentDTO(
            id=_id,
            created_at=date_utils.to_datetime(attributes["createdAt"]),
            updated_at=date_utils.to_datetime(attributes["updatedAt"]),
            amount=attributes["amount"],
            status=attributes["status"],
            description=attributes["description"],
            check_number=attributes.get("checkNumber"),
            originated=attributes["originated"],
            on_us=attributes.get("onUs"),
            on_us_auxiliary=attributes.get("onUsAuxiliary"),
            counterparty_routing_number=attributes.get("counterpartyRoutingNumber"),
            return_status_reason=attributes.get("returnStatusReason"),
            reject_reason=attributes.get("rejectReason"),
            pending_review_reasons=attributes.get("pendingReviewReasons"),
            return_cutoff_time=attributes.get("returnCutoffTime"),
            additional_verification_status=attributes.get("additionalVerificationStatus"),
            tags=attributes.get("tags"),
            delivery_status=attributes.get("deliveryStatus"),
            tracked_at=attributes.get("trackedAt"),
            postal_code=attributes.get("postalCode"),
            expiration_date=attributes.get("expirationDate"),
            expected_delivery=attributes.get("expectedDelivery"),
            send_at=attributes.get("sendAt"),
            counterparty_name=attributes.get("counterparty", {}).get("name"),
            counterparty_moved=attributes.get("counterparty", {}).get("moved"),
            counterparty_street=attributes.get("counterparty", {}).get("address", {}).get("street"),
            counterparty_street2=attributes.get("counterparty", {}).get("address", {}).get("street2"),
            counterparty_city=attributes.get("counterparty", {}).get("address", {}).get("city"),
            counterparty_state=attributes.get("counterparty", {}).get("address", {}).get("state"),
            counterparty_postal_code=attributes.get("counterparty", {}).get("address", {}).get("postalCode"),
            counterparty_country=attributes.get("counterparty", {}).get("address", {}).get("country"),
            memo=attributes.get("memo"),
            relationships=relationships,
        )


class ApproveCheckPaymentRequest(UnitRequest):
    def __init__(self, check_payment_id: str):
        self.check_payment_id = check_payment_id

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "additionalVerification",
            }
        }
        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())
