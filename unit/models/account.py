from unit.utils import date_utils

from unit.models import *

AccountStatus = Literal["Open", "Closed"]
CloseReason = Literal["ByCustomer", "Fraud"]


class DepositAccountDTO(object):
    def __init__(self, id: str, created_at: datetime, name: str, deposit_product: str, routing_number: str,
                 account_number: str, currency: str, balance: int, hold: int, available: int, status: AccountStatus,
                 tags: Optional[Dict[str, str]], close_reason: Optional[CloseReason],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "depositAccount"
        self.attributes = {"name": name, "createdAt": created_at, "depositProduct": deposit_product,
                           "routingNumber": routing_number, "accountNumber": account_number, "currency": currency,
                           "balance": balance, "hold": hold, "available": available, "status": status,
                           "closeReason": close_reason, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DepositAccountDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["name"], attributes["depositProduct"],
            attributes["routingNumber"], attributes["accountNumber"], attributes["currency"], attributes["balance"],
            attributes["hold"], attributes["available"], attributes["status"], attributes.get("tags"),
            attributes.get("closeReason"), relationships
        )


AccountDTO = Union[DepositAccountDTO]


class CreateDepositAccountRequest(UnitRequest):
    def __init__(self, deposit_product: str, relationships: Optional[Dict[str, Union[Relationship, RelationshipArray]]],
                 tags: Optional[Dict[str, str]] = None, idempotency_key: Optional[str] = None):
        self.deposit_product = deposit_product
        self.tags = tags
        self.idempotency_key = idempotency_key
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "depositAccount",
                "attributes": {
                    "depositProduct": self.deposit_product,
                },
                "relationships": self.relationships
            }
        }

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        if self.idempotency_key:
            payload["data"]["attributes"]["idempotencyKey"] = self.idempotency_key

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class PatchDepositAccountRequest(UnitRequest):
    def __init__(self, account_id: str, deposit_product: Optional[str] = None, tags: Optional[Dict[str, str]] = None):
        self.account_id = account_id
        self.deposit_product = deposit_product
        self.tags = tags

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "depositAccount",
                "attributes": {}
            }
        }

        if self.deposit_product:
            payload["data"]["attributes"]["depositProduct"] = self.deposit_product

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class AccountLimitsDTO(object):
    def __init__(self, ach: object, card: object):
        self.type = "limits"
        self.attributes = {"ach": ach, "card": card}

    @staticmethod
    def from_json_api(_type, attributes):
        return AccountLimitsDTO(attributes["ach"], attributes["card"])


class CloseAccountRequest(UnitRequest):
    def __init__(self, account_id: str, reason: Optional[Literal["ByCustomer", "Fraud"]] = "ByCustomer"):
        self.account_id = account_id
        self.reason = reason

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "accountClose",
                "attributes": {
                    "reason": self.reason,
                }
            }
        }

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class ListAccountParams(UnitParams):
    def __init__(self, offset: int = 0, limit: int = 100, customer_id: Optional[str] = None,
                 tags: Optional[object] = None, include: Optional[str] = None):
        self.offset = offset
        self.limit = limit
        self.customer_id = customer_id
        self.tags = tags
        self.include = include
    
    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.tags:
            parameters["filter[tags]"] = self.tags
        if self.include:
            parameters["include"] = self.include
        return parameters
