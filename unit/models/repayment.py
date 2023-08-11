try:
    from typing import Optional, Dict, Union, List, Literal
except ImportError:
    from typing import Optional, Dict, Union, List
    from typing_extensions import Literal

from unit.models import UnitDTO, extract_attributes, UnitRequest, Relationship, UnitParams
from unit.utils import date_utils


class BaseRepayment(UnitDTO):
    def __init__(self, _id, _type, attributes, relationships):
        self.id = _id
        self.type = _type
        self.attributes = extract_attributes(["amount", "status", "tags"], attributes)
        attrs = {"createdAt": date_utils.to_datetime(attributes["createdAt"]),
                 "updatedAt": date_utils.to_datetime(attributes["updatedAt"])}
        self.attributes.update(attrs)
        self.relationships = relationships


class BookRepaymentDTO(BaseRepayment):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BookRepaymentDTO(_id, _type, attributes, relationships)


class AchRepaymentDTO(BaseRepayment):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AchRepaymentDTO(_id, _type, attributes, relationships)


RepaymentDTO = Union[BookRepaymentDTO, AchRepaymentDTO]


class CreateBookRepaymentRequest(UnitRequest):
    def __init__(self, description: str, amount: int, relationships: Dict[str, Relationship],
                 transaction_summary_override: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 idempotency_key: Optional[str] = None):
        self.description = description
        self.amount = amount
        self.transaction_summary_override = transaction_summary_override
        self.tags = tags
        self.idempotency_key = idempotency_key
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        return super().to_payload("bookRepayment", self.relationships)


class CreateAchRepaymentRequest(UnitRequest):
    def __init__(self, description: str, amount: int, relationships: Dict[str, Relationship],
                 addenda: Optional[str] = None, tags: Optional[Dict[str, str]] = None, same_day: Optional[bool] = None,
                 idempotency_key: Optional[str] = None):
        self.description = description
        self.amount = amount
        self.addenda = addenda
        self.tags = tags
        self.same_day = same_day
        self.idempotency_key = idempotency_key
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        return super().to_payload("achRepayment", self.relationships)


CreateRepaymentRequest = Union[CreateBookRepaymentRequest, CreateAchRepaymentRequest]

RepaymentStatus = Literal["Pending", "PendingReview", "Returned", "Sent", "Rejected"]
RepaymentType = Literal["bookRepayment", "achRepayment"]


class ListRepaymentParams(UnitParams):
    def __init__(
        self,
        limit: int = 100,
        offset: int = 0,
        account_id: Optional[str] = None,
        credit_account_id: Optional[str] = None,
        customer_id: Optional[str] = None,
        status: Optional[List[RepaymentStatus]] = None,
        _type: Optional[List[str]] = None,
    ):
        self.limit = limit
        self.offset = offset
        self.account_id = account_id
        self.credit_account_id = credit_account_id
        self.customer_id = customer_id
        self.status = status
        self.type = _type

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}

        if self.account_id:
            parameters["filter[accountId]"] = self.account_id

        if self.credit_account_id:
            parameters["filter[creditAccountId]"] = self.credit_account_id

        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id

        if self.status:
            for idx, status_filter in enumerate(self.status):
                parameters[f"filter[status][{idx}]"] = status_filter

        if self.type:
            for idx, type_filter in enumerate(self.type):
                parameters[f"filter[type][{idx}]"] = type_filter

        return parameters

