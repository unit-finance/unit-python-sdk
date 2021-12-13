from unit.api.base_resource import BaseResource
from unit.models.api_token import *
from unit.models.codecs import DtoDecoder


class APITokenResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "users"

    def create(self, request: CreateAPITokenRequest) -> Union[UnitResponse[APITokenDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.user_id}/api-tokens", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[APITokenDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, user_id: str) -> Union[UnitResponse[List[APITokenDTO]], UnitError]:
        response = super().get(f"{self.resource}/{user_id}/api-tokens")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[APITokenDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def revoke(self, user_id: str, token_id: str) -> Union[UnitResponse, UnitError]:
        response = super().delete(f"{self.resource}/{user_id}/api-tokens/{token_id}")
        if super().is_20x(response.status_code):
            return UnitResponse([], None)
        else:
            return UnitError.from_json_api(response.json())

