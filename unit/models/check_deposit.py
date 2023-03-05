import json
from unit.utils import date_utils
try:
    from typing import Optional, IO, Literal
except ImportError:
    from typing import Optional, IO
    from typing_extensions import Literal
from unit.models import *

CheckDepositStatus = Literal["AwaitingImages", "AwaitingFrontImage", "AwaitingBackImage", "Pending", "PendingReview",
                             "Rejected", "Clearing", "Sent", "Canceled", "Returned"]

class CheckDepositDTO(object):
    def __init__(self, id: str, created_at: datetime, status: str, description: str, amount: str, reason: Optional[str],
                 check_number: Optional[str], counterparty: Optional[CheckCounterparty], settlement_date: Optional[date],
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "checkDeposit"
        self.attributes = {"createdAt": created_at, "status": status, "reason": reason, "description": description,
                           "amount": amount, "checkNumber": check_number, "counterparty": counterparty,
                           "settlementDate": settlement_date, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                               attributes["description"], attributes["amount"], attributes.get("reason"),
                               attributes.get("checkNumber"),
                               CheckCounterparty.from_json_api(attributes.get("counterparty")),
                               date_utils.to_date(attributes.get("settlementDate")), attributes.get("tags"), relationships)


class CreateCheckDepositRequest(UnitRequest):
    def __init__(self, amount: int, relationships: Dict[str, Relationship], description: str,
                 tags: Optional[Dict[str, str]] = None, idempotency_key: Optional[str] = None ):
        self.amount = amount
        self.description = description
        self.tags = tags
        self.idempotency_key = idempotency_key
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "checkDeposit",
                "attributes": {
                    "amount": self.amount,
                    "description": self.description
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
        return json.dumps(self.to_json_api())

class ListCheckDepositParams(UnitParams):
    def __init__(self, offset: int = 0, limit: int = 100, account_id: Optional[str] = None,
                 customer_id: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 sort: Optional[str] = None, include: Optional[str] = None):
        self.offset = offset
        self.limit = limit
        self.account_id = account_id
        self.customer_id = customer_id
        self.tags = tags
        self.sort = sort
        self.include = include

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.account_id:
            parameters["filter[accountId]"] = self.account_id
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.tags:
            parameters["filter[tags]"] = json.dumps(self.tags)
        if self.sort:
            parameters["sort"] = self.sort
        if self.include:
            parameters["include"] = self.include
        return parameters

UploadSide = Literal["front", "back"]

class UploadCheckDepositDocumentRequest(object):
    def __init__(self, check_deposit_id: str, file: IO, side: UploadSide = "front"):
        self.check_deposit_id = check_deposit_id
        self.file = file
        self.side = side


class PatchCheckDepositRequest(UnitRequest):
    def __init__(self, check_deposit_id: str, tags: Optional[Dict[str, str]] = None):
        self.check_deposit_id = check_deposit_id
        self.tags = tags

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "checkDeposit",
                "attributes": {}
            }
        }

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        return json.dumps(self.to_json_api())

