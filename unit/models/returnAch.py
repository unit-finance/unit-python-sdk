import json
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from unit.models import *

AchReturnReason = Literal["InsufficientFunds", "Unauthorized", "UncollectedFunds"]

class ReturnReceivedAchTransactionRequest(UnitRequest):
    def __init__(self, transaction_id: str, reason: AchReturnReason, relationships: [Dict[str, Relationship]]):
        self.transaction_id = transaction_id
        self.reason = reason
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "returnAch",
                "attributes": {
                    "reason": self.reason
                },
                "relationships": self.relationships
            }
        }

        return payload

    def __repr__(self):
        return json.dumps(self.to_json_api())

