from unit.api.base_resource import BaseResource
from unit.models.bill_pay import *
from unit.models.unit_objects import UnitResponse


class BillPayResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "payments/billpay/billers"

    def get(self, params: GetBillersParams) -> Union[UnitResponse[List[BillerDTO]], UnitError]:
        return super().get(self.resource, params.to_dict(), return_type=List[BillerDTO])

