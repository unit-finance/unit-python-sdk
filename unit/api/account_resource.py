from unit.api.base_resource import BaseResource
from unit.models.account import *
from unit.models.unit_objects import UnitResponse


class AccountResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=AccountDTO)
        self.resource = "accounts"

    def create(self, request: CreateDepositAccountRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        return super().post(self.resource, payload)

    def close_account(self, request: CloseAccountRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        return super().post(f"{self.resource}/{request.account_id}/close", payload)

    def reopen_account(self, account_id: str, reason: str = "ByCustomer") -> Union[UnitResponse[AccountDTO], UnitError]:
        return super().post(f"{self.resource}/{account_id}/reopen", {'reason': reason})

    def enter_daca(self, account_id: str) -> Union[UnitResponse[AccountDTO], UnitError]:
        return super().post(f"{self.resource}/{account_id}/enter-daca")

    def activate_daca(self, account_id: str) -> Union[UnitResponse[AccountDTO], UnitError]:
        return super().post(f"{self.resource}/{account_id}/activate-daca")

    def get(self, account_id: str, include: Optional[str] = "") -> Union[UnitResponse[AccountDTO], UnitError]:
        return super().get(f"{self.resource}/{account_id}", {"include": include})

    def list(self, params: ListAccountParams = None) -> Union[UnitResponse[List[AccountDTO]], UnitError]:
        params = params or ListAccountParams()
        return super().get(self.resource, params.to_dict(), return_type=List[AccountDTO])

    def update(self, request: PatchDepositAccountRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        return super().patch(f"{self.resource}/{request.account_id}", payload)

    def limits(self, account_id: str) -> Union[UnitResponse[AccountLimitsDTO], UnitError]:
        return super().get(f"{self.resource}/{account_id}/limits", None)

