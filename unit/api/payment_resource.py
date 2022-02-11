from unit.api.base_resource import BaseResource
from unit.models.payment import *
from unit.models.codecs import DtoDecoder


class PaymentResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "payments"

    def create(self, request: CreatePaymentRequest) -> Union[UnitResponse[PaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(self.resource, payload)
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
            return UnitResponse[PaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(data))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, request: ListPaymentsParams) -> Union[UnitResponse[List[PaymentDTO]], UnitError]:

        parameters = {
            "page[limit]": request.limit,
            "page[offset]": request.offset,
        }
        
        if request.types:
           for idx, type_filter in enumerate(request.types):
               parameters[f"filter[type][{idx}]"] = type_filter
        
        if request.statuses:
           for idx, status_filter in enumerate(request.statuses):
               parameters[f"filter[status][{idx}]"] = status_filter

        response = super().get(self.resource, parameters)
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[PaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(data))
        else:
            return UnitError.from_json_api(response.json())

