import json
from datetime import datetime, date
from typing import Optional, Dict, List
from typing_extensions import Literal

from unit.models import Relationship, UnitParams, UnitRequest
from unit.utils import date_utils


class CounterpartyDTO(object):
    def __init__(self, id: str, created_at: datetime, name: str, routing_number: str, bank: Optional[str],
                 account_number: str, account_type: str, type: str, permissions: str,
                 relationships: [Dict[str, Relationship]]):
        self.id = id
        self.type = "achCounterparty"
        self.attributes = {"createdAt": created_at, "name": name, "routingNumber": routing_number, "bank": bank,
                           "accountNumber": account_number, "accountType": account_type, "type": type,
                           "permissions": permissions}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CounterpartyDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["name"],
                               attributes["routingNumber"], attributes.get("bank"), attributes["accountNumber"],
                               attributes["accountType"], attributes["type"], attributes["permissions"], relationships)


CounterpartyPermissions = Literal["DebitOnly", "CreditAndDebit", "CreditOnly"]
CounterpartyAccountType = Literal["Checking", "Savings", "Loan"]
CounterpartyType = Literal["Business", "Person", "Unknown"]


class CreateCounterpartyRequest(UnitRequest):
    def __init__(self, name: str, routing_number: str, account_number: str, account_type: CounterpartyAccountType,
                 type: CounterpartyType, relationships: [Dict[str, Relationship]], tags: Optional[object] = None,
                 idempotency_key: Optional[str] = None,
                 permissions: Optional[CounterpartyPermissions] = None):
        self.name = name
        self.routing_number = routing_number
        self.account_number = account_number
        self.account_type = account_type
        self.type = type
        self.relationships = relationships
        self.tags = tags
        self.idempotency_key = idempotency_key
        self.permissions = permissions

    def to_json_api(self) -> Dict:
        return super().to_payload("achCounterparty", self.relationships)

    def __repr__(self):
        return json.dumps(self.to_json_api())


class CreateCounterpartyWithTokenRequest(UnitRequest):
    def __init__(self, name: str, type: CounterpartyType, plaid_processor_token: str,
                 relationships: [Dict[str, Relationship]], verify_name: Optional[bool] = None,
                 permissions: Optional[CounterpartyPermissions] = None, tags: Optional[object] = None,
                 idempotency_key: Optional[str] = None):
        self.name = name
        self.type = type
        self.plaid_processor_token = plaid_processor_token
        self.verify_name = verify_name
        self.permissions = permissions
        self.relationships = relationships
        self.tags = tags
        self.idempotency_key = idempotency_key

    def to_json_api(self) -> Dict:
        return super().to_payload("achCounterparty", self.relationships)

    def __repr__(self):
        return json.dumps(self.to_json_api())


class PatchCounterpartyRequest(UnitRequest):
    def __init__(self, counterparty_id: str, plaid_processor_token: str, verify_name: Optional[bool] = None,
                 permissions: Optional[CounterpartyPermissions] = None, tags: Optional[object] = None):
        self.counterparty_id = counterparty_id
        self.plaid_processor_token = plaid_processor_token
        self.verify_name = verify_name
        self.permissions = permissions
        self.tags = tags

    def to_json_api(self) -> Dict:
        return super().to_payload("counterparty", ignore=["counterparty_id"])

    def __repr__(self):
        return json.dumps(self.to_json_api())


class CounterpartyBalanceDTO(object):
    def __init__(self, id: str, balance: int, available: int, relationships: [Dict[str, Relationship]]):
        self.id = id
        self.type = "counterpartyBalance"
        self.attributes = {"balance": balance, "available": available}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CounterpartyBalanceDTO(_id, attributes["balance"], attributes["available"], relationships)


class ListCounterpartyParams(UnitParams):
    def __init__(self, offset: int = 0, limit: int = 100, customer_id: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None, account_number: Optional[str] = None,
                 routing_number: Optional[str] = None, permissions: Optional[List[CounterpartyPermissions]] = None):
        self.offset = offset
        self.limit = limit
        self.customer_id = customer_id
        self.tags = tags
        self.account_number = account_number
        self.routing_number = routing_number
        self.permissions = permissions

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.account_number:
            parameters["filter[accountNumber]"] = self.account_number
        if self.routing_number:
            parameters["filter[routingNumber]"] = self.routing_number
        if self.permissions:
            for idx, p in enumerate(self.permissions):
                parameters[f"filter[permissions][{idx}]"] = p
        if self.tags:
            parameters["filter[tags]"] = json.dumps(self.tags)
        return parameters



