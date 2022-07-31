from unit.api.base_resource import BaseResource
from unit.models.payment import *
from unit.models.unit_objects import UnitResponse

ReturnType = Union[UnitResponse[PaymentDTO], UnitError]


class PaymentResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=PaymentDTO)
        self.resource = "payments"

    def create(self, request: CreatePaymentRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().post(self.resource, payload)

    def update(self, request: PatchPaymentRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().patch(f"{self.resource}/{request.payment_id}", payload)

    def get(self, payment_id: str, include: Optional[str] = "") -> ReturnType:
        return super().get(f"{self.resource}/{payment_id}", {"include": include})

    def list(self, params: ListPaymentParams = None) -> Union[UnitResponse[List[PaymentDTO]], UnitError]:
        params = params or ListPaymentParams()
        return super().get(self.resource, params.to_dict(), return_type=List[PaymentDTO])
