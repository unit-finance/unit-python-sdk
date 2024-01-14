from unit.utils.configuration import Configuration
from unit.api.base_resource import BaseResource
from unit.models.authorization_request import *
from unit.models.codecs import DtoDecoder


class AuthorizationRequestResource(BaseResource):
    def __init__(self, configuration: Configuration):
        super().__init__("authorization-requests", configuration)

    def get(self, authorization_id: str) -> Union[UnitResponse[AuthorizationRequestDTO], UnitError]:
        response = super().get(f"{self.resource}/{authorization_id}")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AuthorizationRequestDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListPurchaseAuthorizationRequestParams = None) \
            -> Union[UnitResponse[List[AuthorizationRequestDTO]], UnitError]:
        params = params or ListPurchaseAuthorizationRequestParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AuthorizationRequestDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def approve(self, request: ApproveAuthorizationRequest) -> Union[UnitResponse[AuthorizationRequestDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.authorization_id}/approve", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AuthorizationRequestDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def decline(self, request: DeclineAuthorizationRequest) -> Union[UnitResponse[AuthorizationRequestDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.authorization_id}/decline", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AuthorizationRequestDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

