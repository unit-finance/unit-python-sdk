import json
from unit.models import *


class AtmLocationDTO(object):
    def __init__(self, network: int, location_name: str, coordinates: Coordinates, address: Address, distance: int,
                 surcharge_free: bool, accept_deposits: bool):
        self.type = "atmLocation"
        self.attributes = {"network": network, "locationName": location_name, "coordinates": coordinates,
                           "address": address, "distance": distance, "surchargeFree": surcharge_free,
                           "acceptDeposits": accept_deposits}

    @staticmethod
    def from_json_api(_type, attributes):
        return AtmLocationDTO(attributes["network"], attributes["locationName"],
                              Coordinates.from_json_api(attributes["coordinates"]),
                              Address.from_json_api(attributes["address"]), attributes["distance"],
                              attributes["surchargeFree"], attributes["acceptDeposits"])


class GetAtmLocationParams(object):
    def __init__(self, search_radius: Optional[int] = None, coordinates: Optional[Coordinates] = None,
                 postal_code: Optional[str] = None, address: Optional[Address] = None):
        self.search_radius = search_radius
        self.coordinates = coordinates
        self.postal_code = postal_code
        self.address = address

