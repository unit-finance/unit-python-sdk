from unit.api.base_resource import BaseResource
from unit.models.authorization import *
from unit.models.unit_objects import UnitResponse


class AuthorizationResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=AuthorizationDTO)
        self.resource = "authorizations"

    def get(self, authorization_id: str, include_non_authorized: Optional[bool] = False) ->\
            Union[UnitResponse[AuthorizationDTO], UnitError]:
        params = {"filter[includeNonAuthorized]": include_non_authorized}
        return super().get(f"{self.resource}/{authorization_id}", params)

    def list(self, params: ListAuthorizationParams = None) -> Union[UnitResponse[List[AuthorizationDTO]], UnitError]:
        params = params or ListAuthorizationParams()
        return super().get(self.resource, params.to_dict(), return_type=List[AuthorizationDTO])
