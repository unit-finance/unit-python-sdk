from unit.utils.configuration import Configuration
from unit.api.base_resource import BaseResource
from unit.models.payment import *
from unit.models.codecs import DtoDecoder


class PaymentResource(BaseResource):
    def __init__(self, configuration: Configuration):
        super().__init__("payments", configuration)

    def create(self, request: CreatePaymentRequest) -> Union[UnitResponse[PaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post_create(self.resource, payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[PaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def update(self, request: PatchPaymentRequest) -> Union[UnitResponse[PaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"{self.resource}/{request.payment_id}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[PaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, payment_id: str, include: Optional[str] = "") -> Union[UnitResponse[PaymentDTO], UnitError]:
        response = super().get(f"{self.resource}/{payment_id}", {"include": include})
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[PaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListPaymentParams = None) -> Union[UnitResponse[List[PaymentDTO]], UnitError]:
        params = params or ListPaymentParams()
        response = super().get(self.resource, params.to_dict())
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            meta = response.json().get("meta")
            return UnitResponse[PaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(included), meta)
        else:
            return UnitError.from_json_api(response.json())

    def create_bulk(self, payments: List[PaymentDTO]) -> Union[UnitResponse[BulkPaymentsDTO], UnitError]:
        response = super().post(f"{self.resource}/bulk", {"data": payments})
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[BulkPaymentsDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def cancel(self, payment_id: str) -> Union[UnitResponse[PaymentDTO], UnitError]:
        response = super().post(f"{self.resource}/{payment_id}/cancel")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[PaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
