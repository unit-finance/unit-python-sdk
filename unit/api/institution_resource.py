from unit.api.base_resource import BaseResource
from unit.models.institution import *
from unit.models.codecs import DtoDecoder


class InstitutionResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "institutions"

    def get(self, routing_number: str) -> Union[UnitResponse[InstitutionDTO], UnitError]:
        response = super().get(f"{self.resource}/{routing_number}", None)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[InstitutionDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
