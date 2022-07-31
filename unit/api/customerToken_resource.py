from unit.api.base_resource import BaseResource
from unit.models.customerToken import *
from unit.models.unit_objects import UnitResponse


class CustomerTokenResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "customers"

    def create_token(self, request: CreateCustomerToken) -> Union[UnitResponse[CustomerTokenDTO], UnitError]:
        payload = request.to_json_api()
        return super().post(f"{self.resource}/{request.customer_id}/token", payload, return_type=CustomerTokenDTO)

    def create_token_verification(self, request: CreateCustomerTokenVerification) ->\
            Union[UnitResponse[CustomerVerificationTokenDTO], UnitError]:
        payload = request.to_json_api()
        return super().post(f"{self.resource}/{request.customer_id}/token/verification", payload,
                            return_type=CustomerVerificationTokenDTO)
