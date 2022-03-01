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


class ListAccountEndOfDayParams(UnitParams):
    def __init__(self, limit: int = 100, offset: int = 0, account_id: Optional[str] = None,
                 customer_id: Optional[str] = None, since: Optional[str] = None, until: Optional[str] = None):
        self.limit = limit
        self.offset = offset
        self.account_id = account_id
        self.customer_id = customer_id
        self.since = since
        self.until = until

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.account_id:
            parameters["filter[accountId]"] = self.account_id
        if self.since:
            parameters["filter[since]"] = self.since
        if self.until:
            parameters["filter[until]"] = self.until
        return parameters

