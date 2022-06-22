from unit.utils import date_utils
from unit.models import *

DisputeStatus = Literal["InvestigationStarted", "ProvisionallyCredited", "Denied", "ResolvedLost", "ResolvedWon"]

class DisputeDTO(object):
    def __init__(self, id: str, source: str, status: str, status_history: Optional[List[DisputeStatus]], description: str,
                 created_at: datetime, updated_at: Optional[datetime], amount: str, decision_reason: Optional[str],
                 relationships):
        self.id = id
        self.type = 'dispute'
        self.attributes = {"source": source, "status": status, "statusHistory": status_history,
                                       "description": description, "createdAt": created_at, "updatedAt": updated_at,
                                       "amount": amount, "decisionReason": decision_reason}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DisputeDTO(_id, attributes.get("source"), attributes.get("status"), attributes.get("statusHistory"),
                          attributes.get("description"), date_utils.to_datetime(attributes["createdAt"]),
                          date_utils.to_datetime(attributes.get("updatedAt")), attributes.get("amount"),
                          attributes.get("decisionReason"), relationships)


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

