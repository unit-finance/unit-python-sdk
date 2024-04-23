from unit.models import *
from unit.utils import date_utils


StopPaymentStatus = Literal["Active", "Disabled"]

class CheckStopPaymentDTO(object):
    def __init__(self, id: str, created_at: datetime, updated_at: datetime, amount: int, status: StopPaymentStatus,
                 check_number: str, tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "checkStopPayment"
        self.attributes = self.attributes = {
            "createdAt": created_at,
            "updatedAt": updated_at,
            "amount": amount,
            "status": status,
            "checkNumber": check_number,
            "tags": tags,
        }
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckStopPaymentDTO(
            id=_id,
            created_at=date_utils.to_datetime(attributes["createdAt"]),
            updated_at=date_utils.to_datetime(attributes["updatedAt"]),
            amount=attributes["amount"],
            status=attributes["status"],
            check_number=attributes["checkNumber"],
            tags=attributes.get("tags"),
            relationships=relationships,
        )
