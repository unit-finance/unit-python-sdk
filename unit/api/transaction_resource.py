from unit.api.base_resource import BaseResource
from unit.models.transaction import *
from unit.models.codecs import DtoDecoder
from unit.models.transaction import *
from unit.api.transaction_resource import ListTransactionsParams



class TransactionResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "transactions"

    def get(self, transaction_id: str) -> Union[UnitResponse[TransactionDTO], UnitError]:
        response = super().get(f"{self.resource}/{transaction_id}")
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[TransactionDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, request: ListTransactionsParams) -> Union[UnitResponse[List[TransactionDTO]], UnitError]:

        args = {
            "page[limit]": request.limit,
            "page[offset]": request.offset,
            "filter[accountId]": request.account_id,
            "filter[customerId]": request.customer_id
        }

        if request.types:
           for idx, type_filter in enumerate(request.types):
               args[f"filter[type][{idx}]"] = type_filter        

        response = super().get(self.resource, args)
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

