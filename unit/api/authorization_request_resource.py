from unit.api.base_resource import BaseResource
from unit.models.authorization_request import *
from unit.models.codecs import DtoDecoder


class AuthorizationRequestResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "authorization-requests"

    def get(self, authorization_id: str) -> Union[UnitResponse[PurchaseAuthorizationRequestDTO], UnitError]:
        response = super().get(f"{self.resource}/{authorization_id}")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[PurchaseAuthorizationRequestDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: PurchaseAuthorizationRequestListParams = PurchaseAuthorizationRequestListParams()) \
            -> Union[UnitResponse[List[PurchaseAuthorizationRequestDTO]], UnitError]:
        parameters = {"page[limit]": params.limit, "page[offset]": params.offset}

        if params.account_id != "":
            parameters |= {"filter[accountId]": params.account_id}

        if params.customer_id != "":
            parameters |= {"filter[customerId]": params.customer_id}

        response = super().get(self.resource, parameters)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[PurchaseAuthorizationRequestDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def approve(self, request: ApproveAuthorizationRequest) -> Union[UnitResponse[PurchaseAuthorizationRequestDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.authorization_id}/approve", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[PurchaseAuthorizationRequestDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def decline(self, request: DeclineAuthorizationRequest) -> Union[UnitResponse[PurchaseAuthorizationRequestDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.authorization_id}/decline", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[PurchaseAuthorizationRequestDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

