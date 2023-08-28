import json
from typing import Optional
from unit.models import *
from unit.utils import date_utils

CheckDepositStatus = Literal[
    "AwaitingImages", "AwaitingFrontImage", "AwaitingBackImage", "Pending", "PendingReview", "Rejected", "Clearing", "Sent", "Canceled", "Returned",
]


class CheckDepositDTO(object):
    def __init__(
        self,
        id: str,
        created_at: datetime,
        status: CheckDepositStatus,
        reason: Optional[str],
        description: str,
        amount: int,
        check_number: str,
        counterparty: Optional[CheckCounterparty],
        settlement_date: Optional[datetime],
        tags: Optional[Dict[str, str]],
        relationships: Dict[str, Relationship]
    ):
        self.id = id
        self.type = "authorization"
        self.attributes = {
            "createdAt": created_at,
            "status": status,
            "description": description,
            "amount": amount,
            "checkNumber": check_number,
        }
        if reason:
            self.attributes["reason"] = reason
        if counterparty:
            self.attributes["counterparty"] = counterparty
        if settlement_date:
            self.attributes["settlementDate"] = settlement_date
        if tags:
            self.attributes["tages"] = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        settlement_date = attributes.get("settlementDate")
        if settlement_date:
            settlement_date = date_utils.to_datetime(settlement_date)

        return CheckDepositDTO(
            id=_id,
            created_at=date_utils.to_datetime(attributes["createdAt"]),
            status=attributes["status"],
            reason=attributes.get("reason"),
            description=attributes["description"],
            amount=attributes["amount"],
            check_number=attributes.get("checkNumber"),
            counterparty=attributes.get("counterparty"),
            settlementDate=settlement_date,
            tags=attributes.get("tags"),
            relationships=relationships,
        )
