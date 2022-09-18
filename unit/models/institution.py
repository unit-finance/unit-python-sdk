from unit.models import *


class InstitutionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return InstitutionDTO(_id, _type, attributes, relationships)

