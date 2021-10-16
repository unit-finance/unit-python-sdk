import json
from typing import Literal, Optional
from models import *


class StatementDTO(object):
    def __init__(self, id: str, period: str, relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = "accountStatementDTO"
        self.attributes = {"period": period}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return StatementDTO(_id, attributes["period"], relationships)

