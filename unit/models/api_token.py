from unit.models import *
from unit.utils import date_utils


class APITokenDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return APITokenDTO(_id, _type, attributes_to_object(attributes), relationships)


class CreateAPITokenRequest(object):
    def __init__(self, user_id: str, description: str, scope: str, expiration: datetime,
                 source_ip: Optional[str] = None):
        # for backward compatibility
        expiration_dt: str = expiration if isinstance(expiration, str) else date_utils.from_datetime(expiration)
        self.user_id = user_id
        self.description = description
        self.scope = scope
        self.expiration = expiration_dt
        self.source_ip = source_ip

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "apiToken",
                "attributes": {
                    "description": self.description,
                    "scope": self.scope,
                    "expiration": self.expiration
                }
            }
        }

        if self.source_ip:
            payload["data"]["attributes"]["sourceIp"] = self.source_ip

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())

