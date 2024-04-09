from unit.utils.configuration import Configuration
from unit.api.base_resource import BaseResource
from unit.models.account_end_of_day import *
from unit.models.codecs import DtoDecoder


class AccountEndOfDayResource(BaseResource):
    def __init__(self, configuration: Configuration):
        super().__init__("account-end-of-day", configuration)

    def list(self, params: ListAccountEndOfDayParams = None) -> Union[UnitResponse[List[AccountEndOfDayDTO]], UnitError]:
        params = params or ListAccountEndOfDayParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AccountEndOfDayDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

