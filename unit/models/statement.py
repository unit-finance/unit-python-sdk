import json
from unit.models import *


class StatementDTO(object):
    def __init__(self, id: str, _type: str, period: str, relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = _type
        self.attributes = {"period": period}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return StatementDTO(_id, _type, attributes["period"], relationships)


OutputType = Literal["html", "pdf"]

class GetStatementParams(object):
    def __init__(self, statement_id: str, output_type: Optional[OutputType] = "html", language: Optional[str] = "en",
                 customer_id: Optional[str] = None):
        self.statement_id = statement_id
        self.output_type = output_type
        self.language = language
        self.customer_id = customer_id


class ListStatementParams(UnitParams):
    def __init__(self, limit: int = 100, offset: int = 0, customer_id: Optional[str] = None,
                 account_id: Optional[str] = None, sort: Optional[Literal["period", "-period"]] = None):
        self.limit = limit
        self.offset = offset
        self.customer_id = customer_id
        self.account_id = account_id
        self.sort = sort

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.account_id:
            parameters["filter[accountId]"] = self.account_id
        if self.sort:
            parameters["sort"] = self.sort
        return parameters

