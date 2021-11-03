from unit.api.base_resource import BaseResource
from unit.models.customerToken import *
from unit.models.codecs import DtoDecoder


class CustomerTokenResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "customers"

    def create_token(self, request: CreateCustomerToken) -> Union[UnitResponse[CustomerTokenDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.customer_id}/token", payload)

        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CustomerTokenDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def create_token_verification(self, request: CreateCustomerTokenVerification) -> Union[UnitResponse[CustomerVerificationTokenDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.customer_id}/token/verification", payload)

        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CustomerVerificationTokenDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
