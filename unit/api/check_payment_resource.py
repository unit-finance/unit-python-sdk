from unit.api.base_resource import BaseResource
from unit.models.authorization_request import *
from unit.models.check_payment import ApproveCheckPaymentRequest, CheckPaymentDTO
from unit.models.codecs import DtoDecoder
from unit.models.payment import CreateCheckPaymentRequest


class CheckPaymentResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "check-payments"

    def get(self, check_payment_id: str) -> Union[UnitResponse[CheckPaymentDTO], UnitError]:
        response = super().get(f"{self.resource}/{check_payment_id}")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[check_payment_id](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def approve(self, request: ApproveCheckPaymentRequest) -> Union[UnitResponse[CheckPaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.check_payment_id}/approve", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CheckPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def create(self, request: CreateCheckPaymentRequest) -> Union[UnitResponse[CheckPaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CheckPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
