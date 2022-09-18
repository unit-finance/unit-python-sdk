from unit.models import *


class DisputeDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DisputeDTO(_id, _type, attributes_to_object(attributes), relationships)


class ListDisputeParams(UnitParams):
    def __init__(self, limit: int = 100, offset: int = 0, query: Optional[str] = None):
        self.limit = limit
        self.offset = offset
        self.query = query

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.query:
            parameters["filter[query]"] = self.query
        return parameters

