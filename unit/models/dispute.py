from unit.utils import date_utils
from unit.models import *

DisputeStatus = Literal["InvestigationStarted", "ProvisionallyCredited", "Denied", "ResolvedLost", "ResolvedWon"]


class DisputeStatusHistory(object):
    def __init__(self, _type: DisputeStatus, updated_at: datetime):
        self.type = _type
        self.updated_at = updated_at

    @staticmethod
    def from_json(data):
        if data is None:
            return None

        dispute_statuses = []
        for history in data:
            dispute_statuses.append(DisputeStatusHistory(history["type"], date_utils.to_datetime(history["updatedAt"])))

        return dispute_statuses


class DisputeDTO(object):
    def __init__(self, _id: str, source: str, status: DisputeStatus,
                 status_history: Optional[List[DisputeStatusHistory]], description: str, created_at: datetime,
                 updated_at: Optional[datetime], amount: str, decision_reason: Optional[str],
                 relationships):
        self.id = _id
        self.type = 'dispute'
        self.attributes = {"source": source, "status": status, "statusHistory": status_history,
                           "description": description, "createdAt": created_at, "updatedAt": updated_at,
                           "amount": amount, "decisionReason": decision_reason}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DisputeDTO(_id, attributes.get("source"), attributes.get("status"),
                          DisputeStatusHistory.from_json(attributes.get("statusHistory")),
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

