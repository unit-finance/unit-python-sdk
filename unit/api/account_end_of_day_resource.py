from unit.api.base_resource import BaseResource
from unit.models.account_end_of_day import *
from unit.models.unit_objects import UnitResponse


class AccountEndOfDayResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "account-end-of-day"

    def list(self, params: ListAccountEndOfDayParams = None) -> Union[UnitResponse[List[AccountEndOfDayDTO]], UnitError]:
        params = params or ListAccountEndOfDayParams()
        return super().get(self.resource, params.to_dict(), return_type=List[AccountEndOfDayDTO])

