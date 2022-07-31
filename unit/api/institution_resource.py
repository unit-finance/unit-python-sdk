from unit.api.base_resource import BaseResource
from unit.models.institution import *
from unit.models.unit_objects import UnitResponse


class InstitutionResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=InstitutionDTO)
        self.resource = "institutions"

    def get(self, routing_number: str) -> Union[UnitResponse[InstitutionDTO], UnitError]:
        return super().get(f"{self.resource}/{routing_number}", None)
