from unit.models import *


class BatchReleaseDTO(object):
    def __init__(self, id: str, amount: int, description: str, sender_name: str, sender_address: Address,
                 sender_account_number: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "batchRelease"
        self.attributes = {
            "amount": amount,
            "description": description,
            "senderName": sender_name,
            "senderAccountNumber": sender_account_number,
            "senderAddress": sender_address,
            "tags": tags,
        }
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BatchReleaseDTO(_id, attributes["amount"], attributes["description"], attributes["senderName"], attributes["senderAddress"], attributes["senderAccountNumber"], attributes.get("tags"), relationships)


class CreateBatchRelease(object):
    def __init__(self, amount: int, description: str, sender_name: str, sender_address: Address,
                 sender_account_number: str, relationships: Optional[Dict[str, Relationship]], tags: Optional[Dict[str, str]] = None,
                 idempotency_key: Optional[str] = None):
        self.amount = amount
        self.description = description
        self.sender_name = sender_name
        self.sender_address = sender_address
        self.sender_account_number = sender_account_number # BIN followed by last four digits?
        self.tags = tags
        self.idempotency_key = idempotency_key
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "type": "batchRelease",
            "attributes": {
                "amount": self.amount,
                "description": self.description,
                "senderName": self.sender_name,
                "senderAccountNumber": self.sender_account_number,
                "senderAddress": self.sender_address
            },
            "relationships": self.relationships
        }

        if self.idempotency_key:
            payload["attributes"]["idempotencyKey"] = self.idempotency_key

        if self.tags:
            payload["attributes"]["tags"] = self.tags

        return payload
