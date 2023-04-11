from unit.utils.configuration import Configuration
from unit.api.base_resource import BaseResource
from unit.models.codecs import DtoDecoder
from unit.models.received_payment import *


class ReceivedPaymentResource(BaseResource):
    def __init__(self, configuration: Configuration):
        super().__init__("received-payments", configuration)
    def update(self, request: PatchReceivedPaymentRequest) -> Union[UnitResponse[AchReceivedPaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"{self.resource}/{request.payment_id}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AchReceivedPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, payment_id: str, include: Optional[str] = "") -> Union[UnitResponse[AchReceivedPaymentDTO], UnitError]:
        response = super().get(f"{self.resource}/{payment_id}", {"include": include})
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[AchReceivedPaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListReceivedPaymentParams = None) -> Union[UnitResponse[List[AchReceivedPaymentDTO]], UnitError]:
        params = params or ListReceivedPaymentParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[AchReceivedPaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def advance(self, payment_id: str) -> Union[UnitResponse[AchReceivedPaymentDTO], UnitError]:
        response = super().post(f"{self.resource}/{payment_id}/advance")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AchReceivedPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())