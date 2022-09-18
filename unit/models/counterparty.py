from unit.models import *


class CounterpartyDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CounterpartyDTO(_id, _type, attributes_to_object(attributes), relationships)


class CreateCounterpartyRequest(object):
    def __init__(self, name: str, routing_number: str, account_number: str, account_type: str, type: str,
                 relationships: [Dict[str, Relationship]], tags: Optional[object] = None,
                 idempotency_key: Optional[str] = None):
        self.name = name
        self.routing_number = routing_number
        self.account_number = account_number
        self.account_type = account_type
        self.type = type
        self.relationships = relationships
        self.tags = tags
        self.idempotency_key = idempotency_key

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

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        if self.idempotency_key:
            payload["data"]["attributes"]["idempotencyKey"] = self.idempotency_key

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class CreateCounterpartyWithTokenRequest(UnitRequest):
    def __init__(self, name: str, _type: str, plaid_processor_token: str, relationships: [Dict[str, Relationship]],
                 verify_name: Optional[bool] = None, permissions: Optional[str] = None, tags: Optional[object] = None,
                 idempotency_key: Optional[str] = None):
        self.name = name
        self.type = _type
        self.plaid_processor_token = plaid_processor_token
        self.verify_name = verify_name
        self.permissions = permissions
        self.relationships = relationships
        self.tags = tags
        self.idempotency_key = idempotency_key

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

        if self.permissions:
            payload["data"]["attributes"]["permissions"] = self.permissions

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        if self.idempotency_key:
            payload["data"]["attributes"]["idempotencyKey"] = self.idempotency_key

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class PatchCounterpartyRequest(object):
    def __init__(self, counterparty_id: str, plaid_processor_token: str, verify_name: Optional[bool] = None,
                 permissions: Optional[str] = None, tags: Optional[object] = None):
        self.counterparty_id = counterparty_id
        self.plaid_processor_token = plaid_processor_token
        self.verify_name = verify_name
        self.permissions = permissions
        self.tags = tags

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

        if self.permissions:
            payload["data"]["attributes"]["permissions"] = self.permissions

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class CounterpartyBalanceDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CounterpartyBalanceDTO(_id, _type, attributes_to_object(attributes), relationships)


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

