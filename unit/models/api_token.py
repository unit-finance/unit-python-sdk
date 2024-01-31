from unit.models import *
from unit.utils import date_utils


class RestrictedResource(UnitDTO):
    def __init__(self, type: str, ids: List[str]):
        self.type = type
        self.ids = ids


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


class CreateAPITokenRequest(UnitRequest):
    def __init__(self, user_id: str, description: str, scope: str, expiration: datetime,
                 source_ip: Optional[str] = None, resources: Optional[List[RestrictedResource]] = None):
        # for backward compatibility
        expiration_dt: str = expiration if isinstance(expiration, str) else date_utils.from_datetime(expiration)
        self.user_id = user_id
        self.description = description
        self.scope = scope
        self.expiration = expiration_dt
        self.source_ip = source_ip
        self.resources = resources

    def to_json_api(self) -> Dict:
        return super().to_payload("apiToken", ignore=["user_id"])

    def __repr__(self):
        return json.dumps(self.to_json_api())

