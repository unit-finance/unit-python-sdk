from unit.utils import date_utils
from unit.models import *
from unit.models import UnitParams


AchReceivedPaymentStatus = Literal["Pending", "Advanced", "Completed", "Returned"]


class AchReceivedPaymentDTO(object):
    def __init__(self, _id: str, created_at: datetime, status: AchReceivedPaymentStatus, was_advanced: bool,
                 is_advanceable: bool, direction: str, completion_date: date, return_reason: Optional[str], amount: int, description: str,
                 addenda: Optional[str], company_name: str, counterparty_routing_number: str, trace_number: str,
                 sec_code: Optional[str], tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        self.id = _id
        self.type = "achReceivedPayment"
        self.attributes = {"createdAt": created_at, "status": status, "wasAdvanced": was_advanced, "isAdvanceable": is_advanceable,
                           "direction": direction, "completionDate": completion_date, "returnReason": return_reason, "description": description,
                           "amount": amount, "addenda": addenda, "companyName": company_name,
                           "counterpartyRoutingNumber": counterparty_routing_number, "traceNumber": trace_number,
                           "secCode": sec_code, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AchReceivedPaymentDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["status"],
                                     attributes["wasAdvanced"], attributes["isAdvanceable"], attributes["direction"], date_utils.to_date(attributes["completionDate"]),
                                     attributes.get("returnReason"), attributes["amount"], attributes["description"],
                                     attributes.get("addenda"), attributes.get("companyName"),
                                     attributes.get("counterpartyRoutingNumber"), attributes.get("traceNumber"),
                                     attributes.get("secCode"), attributes.get("tags"), relationships)


class PatchReceivedPaymentRequest(object):
    def __init__(self, payment_id: str, tags: Dict[str, str]):
        self.payment_id = payment_id
        self.tags = tags

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "achReceivedPayment",
                "attributes": {
                    "tags": self.tags
                }
            }
        }

        return payload

    def __repr__(self):
        return json.dumps(self.to_json_api())


class ListReceivedPaymentParams(UnitParams):
    def __init__(self, limit: int = 100, offset: int = 0, account_id: Optional[str] = None,
                 customer_id: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 status: Optional[List[AchReceivedPaymentStatus]] = None, include_completed: Optional[bool] = None,
                 sort: Optional[Literal["createdAt", "-createdAt"]] = None, include: Optional[str] = None):
        self.limit = limit
        self.offset = offset
        self.account_id = account_id
        self.customer_id = customer_id
        self.tags = tags
        self.status = status
        self.include_completed = include_completed
        self.sort = sort
        self.include = include

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.account_id:
            parameters["filter[accountId]"] = self.account_id
        if self.tags:
            parameters["filter[tags]"] = json.dumps(self.tags)
        if self.include_completed:
            parameters["filter[includeCompleted]"] = self.include_completed
        if self.status:
            for idx, status_filter in enumerate(self.status):
                parameters[f"filter[status][{idx}]"] = status_filter
        if self.sort:
            parameters["sort"] = self.sort
        if self.include:
            parameters["include"] = self.include
        return parameters

