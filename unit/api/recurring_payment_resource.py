from unit.utils.configuration import Configuration
from unit.api.base_resource import BaseResource
from unit.models.payment import *
from unit.models.codecs import DtoDecoder


class RecurringPaymentResource(BaseResource):
    def __init__(self, configuration: Configuration):
        super().__init__("recurring-payments", configuration)

    def create(self, request: CreateRecurringPaymentRequest) -> Union[UnitResponse[RecurringPaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[RecurringPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, payment_id: str, include: Optional[str] = "") -> Union[UnitResponse[RecurringPaymentDTO], UnitError]:
        response = super().get(f"{self.resource}/{payment_id}", {"include": include})
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[RecurringPaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListRecurringPaymentParams = None) -> Union[UnitResponse[List[RecurringPaymentDTO]], UnitError]:
        params = params or ListRecurringPaymentParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[RecurringPaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def disable(self, payment_id: str) -> Union[UnitResponse[RecurringPaymentDTO], UnitError]:
        response = super().post(f"{self.resource}/{payment_id}/disable")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[RecurringPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def enable(self, payment_id: str) -> Union[UnitResponse[RecurringPaymentDTO], UnitError]:
        response = super().post(f"{self.resource}/{payment_id}/enable")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[RecurringPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
