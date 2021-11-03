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

    def close_account(self, account_id: str, reason: Optional[Literal["ByCustomer", "Fraud"]] = "ByCustomer") -> Union[UnitResponse[AccountDTO], UnitError]:
        response = super().post(f"{self.resource}/{account_id}/close", {"attributes": { "reason": reason }})
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

    def get(self, account_id: str) -> Union[UnitResponse[AccountDTO], UnitError]:
        response = super().get(f"{self.resource}/{account_id}", None)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[AccountDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, offset: int = 0, limit: int = 100) -> Union[UnitResponse[list[AccountDTO]], UnitError]:
        response = super().get(self.resource, {"page[limit]": limit, "page[offset]": offset})
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

