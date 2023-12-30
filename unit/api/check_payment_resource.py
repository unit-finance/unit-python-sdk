from unit.utils.configuration import Configuration
from unit.api.base_resource import BaseResource
from unit.models.check_payment import *
from unit.models.codecs import DtoDecoder


class CheckPaymentResource(BaseResource):
    def __init__(self, configuration: Configuration):
        super().__init__("check-payments", configuration)

    def create(self, request: CreateCheckPaymentRequest) -> Union[UnitResponse[CheckPaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post_create(self.resource, payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CheckPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, check_payment_id: str, include: Optional[str] = None) -> Union[UnitResponse[CheckPaymentDTO], UnitError]:
        response = super().get(f"{self.resource}/{check_payment_id}", {"include": include})
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[CheckPaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def download(self, check_payment_id: str, is_back_side: Optional[bool] = True) -> Union[UnitResponse[bytes], UnitError]:
        url = f"{self.resource}/{check_payment_id}" + "/back" if is_back_side else "/front"

        response = super().get(url)
        if super().is_20x(response.status_code):
            return UnitResponse[CheckPaymentDTO](response.content, None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListCheckPaymentParams = None) -> Union[UnitResponse[List[CheckPaymentDTO]], UnitError]:
        params = params or ListCheckPaymentParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[CheckPaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def return_payment(self, request: ReturnCheckPaymentRequest) -> Union[UnitResponse[CheckPaymentDTO], UnitError]:
        payload = request.to_payload()
        response = super().get(f"{self.resource}/{request.check_payment_id}/return", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CheckPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def approve_payment(self, request: ApproveCheckPaymentRequest) -> Union[UnitResponse[CheckPaymentDTO], UnitError]:
        payload = request.to_payload()
        response = super().get(f"{self.resource}/{request.check_payment_id}/approve", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CheckPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def cancel_payment(self, check_payment_id: str) -> Union[UnitResponse[CheckPaymentDTO], UnitError]:
        response = super().post(f"{self.resource}/{check_payment_id}/cancel")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CheckPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
