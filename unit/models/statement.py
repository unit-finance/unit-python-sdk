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

