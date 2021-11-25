import json
from typing import Optional
from unit.models import *


class BillerDTO(object):
    def __init__(self, id: str, name: int, category: str):
        self.id = id
        self.type = "biller"
        self.attributes = {"name": name, "category": category}

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BillerDTO(_id, attributes["name"], attributes["category"])


class GetBillersRequest(object):
    def __init__(self, name: str, page: Optional[int] = None):
        self.name = name
        self.page = page

    def to_json_api(self) -> dict:
        payload = {"name": self.name}

        if self.page:
            payload["page"] = self.page

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())

