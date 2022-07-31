from unit.api.base_resource import BaseResource
from unit.models.fee import *
from unit.models.unit_objects import UnitResponse


class FeeResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=FeeDTO)
        self.resource = "fees"

    def create(self, request: CreateFeeRequest) -> Union[UnitResponse[FeeDTO], UnitError]:
        payload = request.to_json_api()
        return super().post(self.resource, payload)

