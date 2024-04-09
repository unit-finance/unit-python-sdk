from unit.utils.configuration import Configuration
from unit.api.base_resource import BaseResource
from unit.models.account import *
from unit.models.codecs import DtoDecoder


class AccountResource(BaseResource):
    def __init__(self, configuration: Configuration):
        super().__init__("accounts", configuration)

    def create(self, request: CreateAccountRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post_create(self.resource, payload)
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

    def reopen_account(self, account_id: str, reason: AccountCloseReason = "ByCustomer") ->\
            Union[UnitResponse[AccountDTO], UnitError]:
        response = super().post(f"{self.resource}/{account_id}/reopen", {'reason': reason})
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AccountDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def freeze_account(self, request: FreezeAccountRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.account_id}/freeze", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AccountDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def unfreeze_account(self, account_id: str) -> Union[UnitResponse[AccountDTO], UnitError]:
        response = super().post(f"{self.resource}/{account_id}/unfreeze")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AccountDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def enter_daca(self, account_id: str) -> Union[UnitResponse[AccountDTO], UnitError]:
        response = super().post(f"{self.resource}/{account_id}/enter-daca")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AccountDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def activate_daca(self, account_id: str) -> Union[UnitResponse[AccountDTO], UnitError]:
        response = super().post(f"{self.resource}/{account_id}/activate-daca")
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

    def update(self, request: PatchAccountRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
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

    def get_deposit_products(self, account_id: str) -> Union[UnitResponse[List[AccountDepositProductDTO]], UnitError]:
        response = super().get(f"{self.resource}/{account_id}/deposit-products")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            meta = response.json().get("meta")
            return UnitResponse[List[AccountDepositProductDTO]](DtoDecoder.decode(data), meta=meta)
        else:
            return UnitError.from_json_api(response.json())

    def add_owners(self, request: AccountOwnersRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.account_id}/relationships/customers", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AccountDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def remove_owners(self, request: AccountOwnersRequest) -> Union[UnitResponse[AccountDTO], UnitError]:
        payload = request.to_json_api()
        response = super().delete(f"{self.resource}/{request.account_id}/relationships/customers", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AccountDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())