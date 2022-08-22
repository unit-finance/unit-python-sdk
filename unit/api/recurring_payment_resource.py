from unit.api.base_resource import BaseResource
from unit.models.payment import *
from unit.models.codecs import DtoDecoder


class RecurringPaymentResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "recurring-payments"

    def create(self, request: CreateRecurringCreditPaymentRequest) -> Union[UnitResponse[RecurringCreditPaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.payment_id}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[RecurringCreditPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def update(self, request: PatchPaymentRequest) -> Union[UnitResponse[RecurringCreditPaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"{self.resource}/{request.payment_id}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[RecurringCreditAchPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, payment_id: str, include: Optional[str] = "") -> Union[UnitResponse[RecurringCreditPaymentDTO], UnitError]:
        response = super().get(f"{self.resource}/{payment_id}", {"include": include})
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[RecurringCreditPaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListRecurringPaymentParams = None) -> Union[UnitResponse[List[RecurringCreditPaymentDTO]], UnitError]:
        params = params or ListRecurringPaymentParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[RecurringCreditPaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def disable(self, payment_id: str) -> Union[UnitResponse[RecurringCreditPaymentDTO], UnitError]:
        response = super().post(f"{self.resource}/{payment_id}/disable")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[RecurringCreditPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def enable(self, payment_id: str) -> Union[UnitResponse[RecurringCreditPaymentDTO], UnitError]:
        response = super().post(f"{self.resource}/{payment_id}/enable")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[RecurringCreditPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
