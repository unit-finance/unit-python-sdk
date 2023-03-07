from unit.api.base_resource import BaseResource
from unit.models.bill_pay import *
from unit.models.codecs import DtoDecoder


class BillPayResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.resource = "payments/billpay/billers"

    def get(self, params: GetBillersParams) -> Union[UnitResponse[List[BillerDTO]], UnitError]:
        parameters = {"name": params.name}
        if params.page:
            parameters["page"] = params.page

        response = super().get(self.resource, parameters)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[BillerDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

