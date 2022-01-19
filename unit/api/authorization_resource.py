from unit.api.base_resource import BaseResource
from unit.models.authorization import *
from unit.models.codecs import DtoDecoder


class AuthorizationResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "authorizations"

    def get(self, authorization_id: str, include_non_authorized: Optional[bool] = False) -> Union[UnitResponse[AuthorizationDTO], UnitError]:
        params = {"filter[includeNonAuthorized]": include_non_authorized}

        response = super().get(f"{self.resource}/{authorization_id}", params)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AuthorizationDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListAuthorizationParams = None) -> Union[UnitResponse[List[AuthorizationDTO]], UnitError]:
        params = params or ListAuthorizationParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AuthorizationDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
