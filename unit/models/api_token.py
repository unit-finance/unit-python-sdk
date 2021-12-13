from unit.models import *
from unit.utils import date_utils


class APITokenDTO(object):
    def __init__(self, id: str, created_at: datetime, description: str, expiration: datetime, token: Optional[str],
                 source_ip: Optional[str]):
        self.id = id
        self.type = "apiToken"
        self.attributes = {"createdAt": created_at, "description": description, "expiration": expiration,
                           "token": token, "sourceIp": source_ip}

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return APITokenDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["description"],
                           date_utils.to_datetime(attributes["expiration"]), attributes.get("token"),
                           attributes.get("sourceIp"))


class CreateAPITokenRequest(object):
    def __init__(self, user_id: str, description: str, scope: str, expiration: datetime,
                 source_ip: Optional[str] = None):
        self.user_id = user_id
        self.description = description
        self.scope = scope
        self.expiration = expiration
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

