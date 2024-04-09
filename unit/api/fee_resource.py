from unit.utils.configuration import Configuration
from unit.api.base_resource import BaseResource
from unit.models.fee import *
from unit.models.codecs import DtoDecoder


class FeeResource(BaseResource):
    def __init__(self, configuration: Configuration):
        super().__init__("fees", configuration)

    def create(self, request: CreateFeeRequest) -> Union[UnitResponse[FeeDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post_create(self.resource, payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[FeeDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def reverse(self, request: ReverseFeeRequest) -> Union[UnitResponse[FeeDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post_create(f"{self.resource}/reverse", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[FeeDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

