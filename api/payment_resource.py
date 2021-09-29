from api.base_resource import BaseResource
from models.payment import *
from models.codecs import DtoDecoder


class PaymentResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "payments"

    def get(self, payment_id: str) -> Union[UnitResponse[PaymentDTO], UnitError]:
        response = super().get(f"{self.resource}/{payment_id}")
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[PaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(data))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, offset: int = 0, limit: int = 100) -> Union[UnitResponse[list[PaymentDTO]], UnitError]:
        response = super().get(self.resource, {"page[limit]": limit, "page[offset]": offset})
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[PaymentDTO](DtoDecoder.decode(data), DtoDecoder.decode(data))
        else:
            return UnitError.from_json_api(response.json())

