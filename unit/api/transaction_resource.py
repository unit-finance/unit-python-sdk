from unit.api.base_resource import BaseResource
from unit.models.transaction import *
from unit.models.codecs import DtoDecoder
from unit.models.transaction import *


class TransactionResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "transactions"

    def get(self, transaction_id: str, account_id: str, include: Optional[str] = "") -> Union[UnitResponse[TransactionDTO], UnitError]:
        params = {"filter[accountId]": account_id, "include": include}
        response = super().get(f"{self.resource}/{transaction_id}", params)
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[TransactionDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListTransactionParams = None) -> Union[UnitResponse[List[TransactionDTO]], UnitError]:
        params = params or ListTransactionParams()
        response = super().get(self.resource, params.to_dict())
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[TransactionDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def update(self, request: PatchTransactionRequest) -> Union[UnitResponse[TransactionDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"accounts/{request.account_id}/{self.resource}/{request.transaction_id}", payload)
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[TransactionDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def sandbox_simulate_purchase_transaction(self, request: SimulatePurchaseTransaction) -> Union[UnitResponse[PurchaseTransactionDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"sandbox/purchases", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[PurchaseTransactionDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def sandbox_simulate_card_transaction(self, request: SimulateCardTransaction) -> Union[UnitResponse[CardTransactionDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"sandbox/card-transactions", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CardTransactionDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
