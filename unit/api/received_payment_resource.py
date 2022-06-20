from unit.api.base_resource import BaseResource
from unit.models.payment import *
from unit.models.codecs import DtoDecoder


class ReceivedPaymentResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "received-payments"

    def update(self, request: PatchPaymentRequest) -> Union[UnitResponse[AchReceivedPaymentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"{self.resource}/{request.payment_id}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AchReceivedPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, payment_id: str, include: Optional[str] = "") -> Union[UnitResponse[AchReceivedPaymentDTO], UnitError]:
        response = super().get(f"{self.resource}/{payment_id}", {"include": include})
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[AchReceivedPaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(data))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListReceivedPaymentParams = None) -> Union[UnitResponse[List[AchReceivedPaymentDTO]], UnitError]:
        params = params or ListReceivedPaymentParams()
        response = super().get(self.resource, params.to_dict())
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[AchReceivedPaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(data))
        else:
            return UnitError.from_json_api(response.json())

    def advance(self, payment_id: str) -> Union[UnitResponse[AchReceivedPaymentDTO], UnitError]:
        response = super().post(f"{self.resource}/{payment_id}/advance")
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[AchReceivedPaymentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())