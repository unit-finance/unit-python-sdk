from unit.api.base_resource import BaseResource
from unit.models.authorization_request import *
from unit.models.unit_objects import UnitResponse

ReturnType = Union[UnitResponse[PurchaseAuthorizationRequestDTO], UnitError]


class AuthorizationRequestResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=PurchaseAuthorizationRequestDTO)
        self.resource = "authorization-requests"

    def get(self, authorization_id: str) -> ReturnType:
        return super().get(f"{self.resource}/{authorization_id}")

    def list(self, params: ListPurchaseAuthorizationRequestParams = None) \
            -> Union[UnitResponse[List[PurchaseAuthorizationRequestDTO]], UnitError]:
        params = params or ListPurchaseAuthorizationRequestParams()
        return super().get(self.resource, params.to_dict(), return_type=List[PurchaseAuthorizationRequestDTO])

    def approve(self, request: ApproveAuthorizationRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().post(f"{self.resource}/{request.authorization_id}/approve", payload)

    def decline(self, request: DeclineAuthorizationRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().post(f"{self.resource}/{request.authorization_id}/decline", payload)

