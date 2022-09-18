from unit.models import *
from unit.utils import date_utils

PurchaseAuthorizationRequestStatus = Literal["Pending", "Approved", "Declined"]
DeclineReason = Literal["AccountClosed", "CardExceedsAmountLimit", "DoNotHonor", "InsufficientFunds", "InvalidMerchant",
                        "ReferToCardIssuer", "RestrictedCard", "Timeout", "TransactionNotPermittedToCardholder"]


class PurchaseAuthorizationRequestDTO(UnitDTO):
    def __init__(self, _id: str, _type: str, attributes: Dict[str, object], relationships: Dict[str, Relationship]):
        super().__init__(_id, _type, attributes, relationships)
        self.attributes["createdAt"] = date_utils.to_datetime(attributes["createdAt"])

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PurchaseAuthorizationRequestDTO(_id, _type, attributes, relationships)


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
