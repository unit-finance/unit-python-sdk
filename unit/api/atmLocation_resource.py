from unit.api.base_resource import BaseResource
from unit.models.atmLocation import *
from unit.models.codecs import DtoDecoder, UnitEncoder

class AtmLocationResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "atm-locations"

    def get(self, request: GetAtmLocationRequest) -> Union[UnitResponse[list[AtmLocationDTO]], UnitError]:
        params = request.to_json_api()
        # params = {}
        #
        if request.coordinates:
            params["filter[coordinates]"] = json.dumps(request.coordinates, cls=UnitEncoder)

        response = super().get(self.resource, params)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AtmLocationDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

