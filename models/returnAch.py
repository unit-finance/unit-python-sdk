import json
from typing import Literal
from models import *

AchReturnReason = Literal["Unauthorized"]


class ReturnReceivedAchTransactionRequest(object):
    def __init__(self, transaction_id: str, reason: AchReturnReason):
        self.transaction_id = transaction_id
        self.reason = reason

    def to_json_api(self) -> dict:
        payload = {
            "data": {
                "type": "returnAch",
                "attributes": {
                    "reason": self.reason
                }
            }
        }

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())

