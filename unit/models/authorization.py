import json
from typing import Optional
from unit.models import *
from unit.utils import date_utils


class AuthorizationDTO(object):
    def __init__(self, id: str, created_at: datetime, amount: int, card_last_4_digits: str, merchant_name: str,
                 merchant_type: int, merchant_category: str, merchant_location: Optional[str], recurring: bool,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "authorization"
        self.attributes = {"createdAt": created_at, "amount": amount, "cardLast4Digits": card_last_4_digits,
                           "merchant": { "name": merchant_name, "type": merchant_type, "category": merchant_category,
                                         "location": merchant_location}, "recurring": recurring, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["amount"],
                                attributes["cardLast4Digits"], attributes["merchant"]["name"],
                                attributes["merchant"]["type"], attributes["merchant"]["category"],
                                attributes["merchant"].get("location"), attributes["recurring"],
                                attributes.get("tags"), relationships)


class AuthorizationListParams(object):
    def __init__(self, limit: int = 100, offset: int = 0, account_id: str = "", customer_id: str = "",
                 card_id: str = "", since: str = "", until: str = ""):
        self.limit = limit
        self.offset = offset
        self.account_id = account_id
        self.customer_id = customer_id
        self.card_id = card_id
        self.since = since
        self.until = until

