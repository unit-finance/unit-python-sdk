from unit.api.base_resource import BaseResource
from unit.models.atm_location import *
from unit.models.codecs import UnitEncoder
from unit.models.unit_objects import UnitResponse

ReturnType = Union[UnitResponse[List[AtmLocationDTO]], UnitError]


class AtmLocationResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=AtmLocationDTO)
        self.resource = "atm-locations"

    def get(self, request: GetAtmLocationParams) -> ReturnType:
        params = {}

        if request.coordinates:
            params["filter[coordinates]"] = json.dumps(request.coordinates, cls=UnitEncoder)

        if request.address:
            params["filter[address]"] = json.dumps(request.address, cls=UnitEncoder)

        if request.postal_code:
            params["filter[postalCode]"] = json.dumps(request.postal_code, cls=UnitEncoder)

        if request.search_radius:
            params["filter[searchRadius]"] = request.search_radius

        return super().get(self.resource, params)

