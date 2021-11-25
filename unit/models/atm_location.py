import json
from unit.models import *

class AtmLocationDTO(object):
    def __init__(self, attributes: dict):
        self.type = "atmLocation"
        self.attributes = attributes

    @staticmethod
    def from_json_api(_type, attributes):
        return AtmLocationDTO(attributes)


class GetAtmLocationParams(object):
    def __init__(self, search_radius: Optional[int] = None, coordinates: Optional[Coordinates] = None,
                 postal_code: Optional[str] = None, address: Optional[Address] = None):
        self.search_radius = search_radius
        self.coordinates = coordinates
        self.postal_code = postal_code
        self.address = address

