import json
from typing import Optional, Literal
from unit.models import *
from unit.utils import date_utils

PurchaseAuthorizationRequestStatus = Literal["Pending", "Approved", "Declined"]
DeclineReason = Literal["AccountClosed", "CardExceedsAmountLimit", "DoNotHonor", "InsufficientFunds", "InvalidMerchant",
                        "ReferToCardIssuer", "RestrictedCard", "Timeout", "TransactionNotPermittedToCardholder"]

class PurchaseAuthorizationRequestDTO(object):
    def __init__(self, id: str, created_at: datetime, amount: int, status: PurchaseAuthorizationRequestStatus,
                 partial_approval_allowed: str, approved_amount: Optional[int], decline_reason: Optional[DeclineReason],
                 merchant_name: str, merchant_type: int, merchant_category: str, merchant_location: Optional[str],
                 recurring: bool, tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "purchaseAuthorizationRequest"
        self.attributes = {"createdAt": created_at, "amount": amount, "status": status,
                           "partialApprovalAllowed": partial_approval_allowed, "approvedAmount": approved_amount,
                           "declineReason": decline_reason, "merchant": { "name": merchant_name, "type": merchant_type,
                                                                          "category": merchant_category,
                                                                          "location": merchant_location},
                           "recurring": recurring, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PurchaseAuthorizationRequestDTO(_id, date_utils.to_datetime(attributes["createdAt"]),
                                               attributes["amount"], attributes["status"],
                                               attributes.get("partialApprovalAllowed"),
                                               attributes.get("approvedAmount"), attributes.get("declineReason"),
                                               attributes["merchant"]["name"], attributes["merchant"]["type"],
                                               attributes["merchant"]["category"],
                                               attributes["merchant"].get("location"), attributes["recurring"],
                                               attributes.get("tags"), relationships)


class ListPurchaseAuthorizationRequestParams(object):
    def __init__(self, limit: int = 100, offset: int = 0, account_id: Optional[str] = None,
                 customer_id: Optional[str] = None):
        self.limit = limit
        self.offset = offset
        self.account_id = account_id
        self.customer_id = customer_id

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.account_id:
            parameters["filter[accountId]"] = self.account_id
        return parameters


class ApproveAuthorizationRequest(object):
    def __init__(self, authorization_id: str, amount: Optional[int] = None, tags: Optional[Dict[str, str]] = None):
        self.authorization_id = authorization_id
        self.amount = amount
        self.tags = tags

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "approveAuthorizationRequest",
                "attributes": {}
            }
        }

        if self.amount:
            payload["data"]["attributes"]["amount"] = self.amount

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class DeclineAuthorizationRequest(object):
    def __init__(self, authorization_id: str, reason: DeclineReason):
        self.authorization_id = authorization_id
        self.reason = reason

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "declineAuthorizationRequest",
                "attributes": {
                    "reason": self.reason
                }
            }
        }

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())
