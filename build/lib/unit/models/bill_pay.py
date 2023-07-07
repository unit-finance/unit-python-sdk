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


class GetBillersParams(object):
    def __init__(self, name: str, page: Optional[int] = None):
        self.name = name
        self.page = page

