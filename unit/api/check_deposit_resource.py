from unit.api.base_resource import BaseResource
from unit.models.check_deposit import *
from unit.models.codecs import DtoDecoder
from unit.models.transaction import *


class CheckDepositResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "check-deposits"

    def get(self, check_deposit_id: str) -> Union[UnitResponse[CheckDepositDTO], UnitError]:
        params = {}
        response = super().get(f"{self.resource}/{check_deposit_id}", params)
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[TransactionDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListTransactionParams = None) -> Union[UnitResponse[List[CheckDepositDTO]], UnitError]:
        raise NotImplementedError()
