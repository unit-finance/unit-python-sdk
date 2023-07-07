from unit.api.base_resource import BaseResource
from unit.models.atm_location import *
from unit.models.codecs import DtoDecoder, UnitEncoder

class AtmLocationResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "atm-locations"

    """
    UnitEncoder must be imported here and not in the model class to no cause circular importing.
    """
    def get(self, request: GetAtmLocationParams) -> Union[UnitResponse[List[AtmLocationDTO]], UnitError]:
        params = {}

        if request.coordinates:
            params["filter[coordinates]"] = json.dumps(request.coordinates, cls=UnitEncoder)

        if request.address:
            params["filter[address]"] = json.dumps(request.address, cls=UnitEncoder)

        if request.postal_code:
            params["filter[postalCode]"] = json.dumps(request.postal_code, cls=UnitEncoder)

        if request.search_radius:
            params["filter[searchRadius]"] = request.search_radius

        response = super().get(self.resource, params)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AtmLocationDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

