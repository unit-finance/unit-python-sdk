import json
from typing import Optional
from unit.models import *


class AccountEndOfDayDTO(object):
    def __init__(self, id: str, date: str, balance: int, hold: int, available: int,
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "accountEndOfDay"
        self.attributes = {"date": date, "balance": balance, "hold": hold, "available": available}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountEndOfDayDTO(_id, attributes["date"], attributes["balance"], attributes["hold"],
                                  attributes["available"], relationships)


class AccountEndOfDayListParams(object):
    def __init__(self, limit: int = 100, offset: int = 0, account_id: str = "", customer_id: str = "", since: str = "",
                 until: str = ""):
        self.limit = limit
        self.offset = offset
        self.account_id = account_id
        self.customer_id = customer_id
        self.since = since
        self.until = until