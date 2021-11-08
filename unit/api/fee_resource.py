from unit.api.base_resource import BaseResource
from unit.models.fee import *
from unit.models.codecs import DtoDecoder


class FeeResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "fees"

    def create(self, request: CreateFeeRequest) -> Union[UnitResponse[FeeDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(self.resource, payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[FeeDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

