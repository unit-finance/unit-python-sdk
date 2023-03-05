import json
try:
    from typing import Optional, Literal, Dict, List
except:
    from typing import Optional, Dict, List
    from typing_extensions import Literal
from datetime import datetime
from unit.models import Relationship, UnitRequest, UnitParams
from unit.utils import create_relationship, create_deposit_account_relationship, date_utils

SORT_ORDERS = Literal["created_at", "-created_at"]
RELATED_RESOURCES = Literal["customer", "account", "transaction"]
RewardStatus = Literal["Sent", "Rejected"]


class RewardDTO(object):
    def __init__(self, _id: str, created_at: datetime, amount: int, description: str, status: RewardStatus,
                 reject_reason: Optional[str], tags: Optional[Dict[str, str]] = None,
                 relationships: Optional[Dict[str, Relationship]] = None):
        self.id = _id
        self.type = "reward"
        self.attributes = {"createdAt": created_at, "amount": amount, "description": description, "status": status,
                           "rejectReason": reject_reason, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, attributes, relationships):
        return RewardDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["amount"],
                         attributes["description"], attributes["status"], attributes.get("rejectReason"),
                         attributes.get("tags"), relationships)


class CreateRewardRequest(UnitRequest):
    def __init__(
        self,
        amount: int,
        description: str,
        receiving_account_id: str,
        rewarded_transaction_id: Optional[str] = None,
        funding_account_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None
    ):
        self.type = "reward"
        self.amount = amount
        self.description = description
        self.rewarded_transaction_id = rewarded_transaction_id
        self.receiving_account_id = receiving_account_id
        self.funding_account_id = funding_account_id
        self.idempotency_key = idempotency_key
        self.tags = tags

        self.relationships = create_deposit_account_relationship(self.receiving_account_id, "receivingAccount")

        if self.rewarded_transaction_id:
            self.relationships.update(
                create_relationship("transaction", self.rewarded_transaction_id, "rewardedTransaction"))

        if self.funding_account_id:
            self.relationships.update(
                create_deposit_account_relationship(self.funding_account_id, "fundingAccount"))

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": self.type,
                "attributes": {
                    "amount": self.amount,
                    "description": self.description
                },
                "relationships": self.relationships
            }
        }

        if self.idempotency_key:
            payload["data"]["attributes"]["idempotencyKey"] = self.idempotency_key

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        return json.dumps(self.to_json_api())


class ListRewardsParams(UnitParams):
    def __init__(
        self,
        limit: int = 100,
        offset: int = 0,
        transaction_id: Optional[str] = None,
        rewarded_transaction_id: Optional[str] = None,
        receiving_account_id: Optional[str] = None,
        customer_id: Optional[str] = None,
        card_id: Optional[str] = None,
        status: Optional[str] = None,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        sort: Optional[SORT_ORDERS] = None,
        include: Optional[List[RELATED_RESOURCES]] = None,
        tags: Optional[Dict[str, str]] = None,
    ):
        self.limit = limit
        self.offset = offset
        self.transaction_id = transaction_id
        self.rewarded_transaction_id = rewarded_transaction_id
        self.receiving_account_id = receiving_account_id
        self.customer_id = customer_id
        self.card_id = card_id
        self.status = status
        self.since = since
        self.until = until
        self.sort = sort
        self.include = include
        self.tags = tags

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}

        if self.transaction_id:
            parameters["filter[transactionId]"] = self.transaction_id

        if self.rewarded_transaction_id:
            parameters["filter[rewardedTransactionId]"] = self.rewarded_transaction_id

        if self.receiving_account_id:
            parameters["filter[receivingAccountId]"] = self.receiving_account_id

        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id

        if self.card_id:
            parameters["filter[cardId]"] = self.card_id

        if self.status:
            parameters["filter[status]"] = self.status

        if self.since:
            parameters["filter[since]"] = self.since

        if self.until:
            parameters["filter[until]"] = self.until

        if self.sort:
            parameters["sort"] = self.sort

        if self.tags:
            parameters["filter[tags]"] = json.dumps(self.tags)

        return parameters

