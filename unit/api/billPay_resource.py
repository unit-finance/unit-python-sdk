from unit.api.base_resource import BaseResource
from unit.models.billPay import *
from unit.models.codecs import DtoDecoder


class BillPayResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "payments/billpay/billers"

    def get(self, request: GetBillersRequest) -> Union[UnitResponse[list[BillerDTO]], UnitError]:
        params = request.to_json_api()
        response = super().get(self.resource, params)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[BillerDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

