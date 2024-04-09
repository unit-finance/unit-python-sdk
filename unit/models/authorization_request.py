import json
try:
    from typing import Optional, Literal
except ImportError:
    from typing import Optional
    from typing_extensions import Literal
from unit.models import *
from unit.utils import date_utils

PurchaseAuthorizationRequestStatus = Literal["Pending", "Approved", "Declined"]
DeclineReason = Literal["AccountClosed", "CardExceedsAmountLimit", "DoNotHonor", "InsufficientFunds", "InvalidMerchant",
                        "ReferToCardIssuer", "RestrictedCard", "Timeout", "TransactionNotPermittedToCardholder"]


class BaseAuthorizationRequest(object):
    def __init__(self, id: str, type: str, attributes: Dict[str, object],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = type
        self.attributes = {"createdAt": date_utils.to_datetime(attributes["createdAt"]), "amount": attributes["amount"],
                           "status": attributes["status"],
                           "partialApprovalAllowed": attributes.get("partialApprovalAllowed"),
                           "approvedAmount": attributes.get("approvedAmount"),
                           "declineReason": attributes.get("declineReason"),
                           "cardNetwork": attributes.get("cardNetwork"), "tags": attributes.get("tags")}
        self.relationships = relationships


class PurchaseAuthorizationRequestDTO(BaseAuthorizationRequest):
    def __init__(self, id: str, attributes: Dict[str, object], relationships: Optional[Dict[str, Relationship]]):
        super().__init__(id, "purchaseAuthorizationRequest", attributes, relationships)
        self.attributes.update({"recurring": attributes.get("recurring"), "ecommerce": attributes.get("ecommerce"),
                                "cardPresent": attributes.get("cardPresent"),
                                "paymentMethod": attributes.get("paymentMethod"),
                                "digitalWallet": attributes.get("digitalWallet"),
                                "cardVerificationData": attributes.get("cardVerificationData"),
                                "merchant": Merchant.from_json_api(attributes["merchant"]),
                                "healthcareAmounts":
                                    HealthcareAmounts.from_json_api(attributes.get("healthcareAmounts")),
                                "cashWithdrawalAmount": attributes.get("cashWithdrawalAmount")})

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PurchaseAuthorizationRequestDTO(_id, attributes, relationships)


class CardTransactionAuthorizationRequestDTO(BaseAuthorizationRequest):
    def __init__(self, id: str, attributes: Dict[str, object], relationships: Optional[Dict[str, Relationship]]):
        super().__init__(id, "cardTransactionAuthorizationRequest", attributes, relationships)
        self.attributes.update({"recurring": attributes.get("recurring"),
                                "paymentMethod": attributes.get("paymentMethod"),
                                "digitalWallet": attributes.get("digitalWallet"),
                                "cardVerificationData": attributes.get("cardVerificationData"),
                                "merchant": Merchant.from_json_api(attributes["merchant"])})

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardTransactionAuthorizationRequestDTO(_id, attributes, relationships)


class AtmAuthorizationRequestDTO(BaseAuthorizationRequest):
    def __init__(self, id: str, attributes: Dict[str, object], relationships: Optional[Dict[str, Relationship]]):
        super().__init__(id, "atmAuthorizationRequest", attributes, relationships)
        self.attributes.update({"atmName": attributes["atmName"], "atmLocation": attributes.get("atmLocation"),
                                "surcharge": attributes["surcharge"], "direction": attributes.get("direction"),
                                "internationalServiceFee": attributes.get("internationalServiceFee")})

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AtmAuthorizationRequestDTO(_id, attributes, relationships)


AuthorizationRequestDTO = Union[PurchaseAuthorizationRequestDTO, CardTransactionAuthorizationRequestDTO,
                                AtmAuthorizationRequestDTO]

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


class ApproveAuthorizationRequest(UnitRequest):
    def __init__(self, authorization_id: str, amount: Optional[int] = None, tags: Optional[Dict[str, str]] = None,
                 funding_account: Optional[str] = None):
        self.authorization_id = authorization_id
        self.amount = amount
        self.tags = tags
        self.funding_account = funding_account

    def to_json_api(self) -> Dict:
        return super().to_payload("approveAuthorizationRequest", ignore=["authorization_id"])

    def __repr__(self):
        return json.dumps(self.to_json_api())


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
        return json.dumps(self.to_json_api())
