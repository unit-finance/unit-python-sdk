import json
from typing import Optional
from unit.models import *


class InstitutionDTO(object):
    def __init__(self, routing_number: str, name: str, is_ach_supported: bool, is_wire_supported: bool,
                 address: Optional[Address] = None):
        self.type = "institution"
        self.attributes = {"routingNumber": routing_number, "name": name, "address": address,
                           "isACHSupported": is_ach_supported, "isWireSupported": is_wire_supported}

    def from_json_api(_id, _type, attributes, relationships):
        return InstitutionDTO(
            attributes["routingNumber"], attributes["name"], attributes["isACHSupported"],
            attributes["isWireSupported"], attributes.get("address"))

