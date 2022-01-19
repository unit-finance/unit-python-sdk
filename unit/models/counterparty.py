import json
from datetime import datetime, date
from typing import Optional
from unit.utils import date_utils
from unit.models import *


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


class CreateCounterpartyRequest(object):
    def __init__(self, name: str, routing_number: str, account_number: str, account_type: str, type: str,
                 relationships: [Dict[str, Relationship]]):
        self.name = name
        self.routing_number = routing_number
        self.account_number = account_number
        self.account_type = account_type
        self.type = type
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "achCounterparty",
                "attributes": {
                    "name": self.name,
                    "routingNumber": self.routing_number,
                    "accountNumber": self.account_number,
                    "accountType": self.account_type,
                    "type": self.type
                },
                "relationships": self.relationships
            }
        }

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class CreateCounterpartyWithTokenRequest(UnitRequest):
    def __init__(self, name: str, type: str, plaid_processor_token: str, verify_name: Optional[bool],
                 relationships: [Dict[str, Relationship]]):
        self.name = name
        self.type = type
        self.plaid_processor_token = plaid_processor_token
        self.verify_name = verify_name
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "achCounterparty",
                "attributes": {
                    "name": self.name,
                    "type": self.type,
                    "plaidProcessorToken": self.plaid_processor_token
                },
                "relationships": self.relationships
            }
        }

        if self.verify_name:
            payload["data"]["attributes"]["verifyName"] = self.verify_name

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class PatchCounterpartyRequest(object):
    def __init__(self, counterparty_id: str, plaid_processor_token: str, verify_name: Optional[bool] = False):
        self.counterparty_id = counterparty_id
        self.plaid_processor_token = plaid_processor_token
        self.verify_name = verify_name

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "counterparty",
                "attributes": {
                    "plaidProcessorToken": self.plaid_processor_token
                }
            }
        }

        if self.verify_name:
            payload["data"]["attributes"]["verifyName"] = self.verify_name

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


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
                 tags: Optional[object] = None):
        self.offset = offset
        self.limit = limit
        self.customer_id = customer_id
        self.tags = tags

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.tags:
            parameters["filter[tags]"] = self.tags
        return parameters

