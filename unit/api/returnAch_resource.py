from unit.api.base_resource import BaseResource
from unit.models.transaction import ReturnedReceivedAchTransactionDTO
from unit.models.returnAch import *
from unit.models.unit_objects import UnitResponse


class ReturnAchResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "returns"

    def return_ach(self, request: ReturnReceivedAchTransactionRequest) ->\
            Union[UnitResponse[ReturnedReceivedAchTransactionDTO], UnitError]:
        payload = request.to_json_api()
        return super().post(f"{self.resource}/{request.transaction_id}", payload,
                            return_type=ReturnedReceivedAchTransactionDTO)
