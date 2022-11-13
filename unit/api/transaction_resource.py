from unit.api.base_resource import BaseResource
from unit.models.codecs import DtoDecoder
from unit.models.transaction import *


class TransactionResource(BaseResource):
    def __init__(self, api_url, token, retries):
        super().__init__(api_url, token, retries)
        self.resource = "transactions"

    def get(self, transaction_id: str, include: Optional[str] = "") -> Union[UnitResponse[TransactionDTO], UnitError]:
        response = super().get(f"{self.resource}/{transaction_id}", {"include": include})
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[TransactionDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListTransactionParams = None) -> Union[UnitResponse[List[TransactionDTO]], UnitError]:
        params = params or ListTransactionParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[TransactionDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def update(self, request: PatchTransactionRequest) -> Union[UnitResponse[TransactionDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"accounts/{request.account_id}/{self.resource}/{request.transaction_id}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[TransactionDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def get_by_id_and_account(self, transaction_id: str, account_id: str, include: Optional[str] = "") ->\
            Union[UnitResponse[TransactionDTO], UnitError]:
        response = super().get(f"accounts/{account_id}/{self.resource}/{transaction_id}", {"include": include})
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[TransactionDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())
