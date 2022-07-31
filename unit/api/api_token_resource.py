from unit.api.base_resource import BaseResource
from unit.models.api_token import *
from unit.models.unit_objects import UnitResponse

ReturnType = Union[UnitResponse[APITokenDTO], UnitError]


class APITokenResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=APITokenDTO)
        self.resource = "users"

    def create(self, request: CreateAPITokenRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().post(f"{self.resource}/{request.user_id}/api-tokens", payload)

    def list(self, user_id: str) -> Union[UnitResponse[List[APITokenDTO]], UnitError]:
        return super().get(f"{self.resource}/{user_id}/api-tokens", return_type=List[APITokenDTO])

    def revoke(self, user_id: str, token_id: str) -> ReturnType:
        return super().delete(f"{self.resource}/{user_id}/api-tokens/{token_id}")

