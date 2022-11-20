from unit.api.base_resource import BaseResource
from unit.models.account_end_of_day import *
from unit.models.unit_models import UnitResponse


class AccountEndOfDayResource(BaseResource):
    def __init__(self, api_url, token, retries):
        super().__init__(api_url, token, retries)
        self.resource = "account-end-of-day"

    def list(self, params: ListAccountEndOfDayParams = None) -> Union[UnitResponse[List[AccountEndOfDayDTO]], UnitError]:
        params = params or ListAccountEndOfDayParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            return UnitResponse.from_json_api(response.json())
        else:
            return UnitError.from_json_api(response.json())

