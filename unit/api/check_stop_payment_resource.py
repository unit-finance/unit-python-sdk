from unit.api.base_resource import BaseResource
from unit.models.authorization_request import *
from unit.models.check_stop_payment import CheckStopPaymentDTO
from unit.models.codecs import DtoDecoder
from unit.models.payment import CreateCheckStopPaymentRequest


class CheckStopPaymentResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "stop-payments"

    def create(self, request: CreateCheckStopPaymentRequest) -> Union[UnitResponse[CheckStopPaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CheckStopPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
