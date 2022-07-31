from unit.api.base_resource import BaseResource
from unit.models.transaction import *
from unit.models.unit_objects import UnitResponse


class TransactionResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=TransactionDTO)
        self.resource = "transactions"

    def get(self, transaction_id: str, include: Optional[str] = "") -> Union[UnitResponse[TransactionDTO], UnitError]:
        return super().get(f"{self.resource}/{transaction_id}", {"include": include})

    def list(self, params: ListTransactionParams = None) -> Union[UnitResponse[List[TransactionDTO]], UnitError]:
        params = params or ListTransactionParams()
        return super().get(self.resource, params.to_dict(), return_type=List[TransactionDTO])

    def update(self, request: PatchTransactionRequest) -> Union[UnitResponse[TransactionDTO], UnitError]:
        payload = request.to_json_api()
        return super().patch(f"accounts/{request.account_id}/{self.resource}/{request.transaction_id}", payload)
