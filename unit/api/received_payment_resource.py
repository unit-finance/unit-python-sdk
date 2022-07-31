from unit.api.base_resource import BaseResource
from unit.models.payment import *
from unit.models.unit_objects import UnitResponse

ReturnType = Union[UnitResponse[AchReceivedPaymentDTO], UnitError]


class ReceivedPaymentResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "received-payments"

    def update(self, request: PatchPaymentRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().patch(f"{self.resource}/{request.payment_id}", payload)

    def get(self, payment_id: str, include: Optional[str] = "") -> ReturnType:
        return super().get(f"{self.resource}/{payment_id}", {"include": include})

    def list(self, params: ListReceivedPaymentParams = None) ->\
            Union[UnitResponse[List[AchReceivedPaymentDTO]], UnitError]:
        params = params or ListReceivedPaymentParams()
        return super().get(self.resource, params.to_dict(), return_type=List[AchReceivedPaymentDTO])

    def advance(self, payment_id: str) -> ReturnType:
        return super().post(f"{self.resource}/{payment_id}/advance")