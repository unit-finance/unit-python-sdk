from unit.api.base_resource import BaseResource
from unit.models.authorization_request import *
from unit.models.check_payment import ApproveCheckPaymentRequest, CheckPaymentDTO
from unit.models.codecs import DtoDecoder


class CheckPaymentResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "check-payments"

    def approve(self, request: ApproveCheckPaymentRequest) -> Union[UnitResponse[CheckPaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.check_payment_id}/approve", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CheckPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
