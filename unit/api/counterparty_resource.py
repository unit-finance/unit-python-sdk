from unit.api.base_resource import BaseResource
from unit.models.counterparty import *
from unit.models.unit_objects import UnitResponse

ReturnType = Union[UnitResponse[CounterpartyDTO], UnitError]


class CounterpartyResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=CounterpartyDTO)
        self.resource = "counterparties"

    def create(self, request: Union[CreateCounterpartyRequest, CreateCounterpartyWithTokenRequest]) -> ReturnType:
        payload = request.to_json_api()
        return super().post(self.resource, payload)

    def update(self, request: PatchCounterpartyRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().patch(f"{self.resource}/{request.counterparty_id}", payload)

    def delete(self, counterparty_id: str) -> Union[UnitResponse, UnitError]:
        return super().delete(f"{self.resource}/{counterparty_id}", return_type=List)

    def get(self, counterparty_id: str) -> ReturnType:
        return super().get(f"{self.resource}/{counterparty_id}")

    def list(self, params: ListCounterpartyParams = None) -> Union[UnitResponse[List[CounterpartyDTO]], UnitError]:
        params = params or ListCounterpartyParams()
        return super().get(self.resource, params.to_dict(), return_type=List[CounterpartyDTO])

    def get_balance(self, counterparty_id: str) -> Union[UnitResponse[CounterpartyBalanceDTO], UnitError]:
        return super().get(f"{self.resource}/{counterparty_id}/balance", return_type=CounterpartyBalanceDTO)
