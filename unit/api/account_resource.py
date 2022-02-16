from unit.api.base_resource import BaseResource
from unit.models.account import *
from unit.models.codecs import DtoDecoder

class AccountResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "accounts"

    def create(self, request: CreateDepositAccountRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(self.resource, payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AccountDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def close_account(self, request: CloseAccountRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.account_id}/close", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AccountDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def reopen_account(self, account_id: str, reason: str = "ByCustomer") -> Union[UnitResponse[AccountDTO], UnitError]:
        response = super().post(f"{self.resource}/{account_id}/reopen", {'reason': reason})
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AccountDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, account_id: str, include: Optional[str] = "") -> Union[UnitResponse[AccountDTO], UnitError]:
        response = super().get(f"{self.resource}/{account_id}", {"include": include})
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[AccountDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListAccountParams = None) -> Union[UnitResponse[List[AccountDTO]], UnitError]:
        params = params or ListAccountParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[AccountDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def update(self, request: PatchDepositAccountRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"{self.resource}/{request.account_id}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AccountDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def limits(self, account_id: str) -> Union[UnitResponse[AccountLimitsDTO], UnitError]:
        response = super().get(f"{self.resource}/{account_id}/limits", None)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AccountLimitsDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

