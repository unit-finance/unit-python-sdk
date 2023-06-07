from unit.utils.configuration import Configuration
from unit.api.base_resource import BaseResource
from unit.models.account import *


class AccountResource(BaseResource):
    def __init__(self, configuration: Configuration):
        super().__init__("accounts", configuration)

    def create(self, request: CreateAccountRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post_create(self.resource, payload)
        return super().create_response(response)

    def close_account(self, request: CloseAccountRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.account_id}/close", payload)
        return super().create_response(response)

    def reopen_account(self, account_id: str, reason: AccountCloseReason = "ByCustomer") ->\
            Union[UnitResponse[AccountDTO], UnitError]:
        response = super().post(f"{self.resource}/{account_id}/reopen", {'reason': reason})
        return super().create_response(response)

    def freeze_account(self, request: FreezeAccountRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.account_id}/freeze", payload)
        return super().create_response(response)

    def unfreeze_account(self, account_id: str) -> Union[UnitResponse[AccountDTO], UnitError]:
        response = super().post(f"{self.resource}/{account_id}/unfreeze")
        return super().create_response(response)

    def enter_daca(self, account_id: str) -> Union[UnitResponse[AccountDTO], UnitError]:
        response = super().post(f"{self.resource}/{account_id}/enter-daca")
        return super().create_response(response)

    def activate_daca(self, account_id: str) -> Union[UnitResponse[AccountDTO], UnitError]:
        response = super().post(f"{self.resource}/{account_id}/activate-daca")
        return super().create_response(response)

    def get(self, account_id: str, include: Optional[str] = "") -> Union[UnitResponse[AccountDTO], UnitError]:
        response = super().get(f"{self.resource}/{account_id}", {"include": include})
        return super().create_response(response)

    def list(self, params: ListAccountParams = None) -> Union[UnitResponse[List[AccountDTO]], UnitError]:
        params = params or ListAccountParams()
        response = super().get(self.resource, params.to_dict())
        return super().create_response(response)

    def update(self, request: PatchAccountRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"{self.resource}/{request.account_id}", payload)
        return super().create_response(response)

    def limits(self, account_id: str) -> Union[UnitResponse[AccountLimitsDTO], UnitError]:
        response = super().get(f"{self.resource}/{account_id}/limits", None)
        return super().create_response(response)

    def get_deposit_products(self, account_id: str) -> Union[UnitResponse[List[AccountDepositProductDTO]], UnitError]:
        response = super().get(f"{self.resource}/{account_id}/deposit-products")
        return super().create_response(response)

    def add_owners(self, request: AccountOwnersRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.account_id}/relationships/customers", payload)
        return super().create_response(response)

    def remove_owners(self, request: AccountOwnersRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        response = super().delete(f"{self.resource}/{request.account_id}/relationships/customers", payload)
        return super().create_response(response)
