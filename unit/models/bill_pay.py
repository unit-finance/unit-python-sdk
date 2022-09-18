from unit.models import *


class BillerDTO(UnitDTO):
    def __init__(self, _id: str, _type: str, attributes: Dict[str, object], relationships: Dict[str, Relationship]):
        super().__init__(_id, _type, attributes, relationships)

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BillerDTO(_id, _type, attributes, relationships)


class GetBillersParams(object):
    def __init__(self, name: str, page: Optional[int] = None):
        self.name = name
        self.page = page

