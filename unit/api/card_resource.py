from unit.api.base_resource import BaseResource
from unit.models.card import *
from unit.models.unit_objects import UnitResponse

ReturnType = Union[UnitResponse[Card], UnitError]


class CardResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=Card)
        self.resource = "cards"

    def create(self, request: CreateCardRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().post(self.resource, payload)

    def report_stolen(self, card_id: str) -> ReturnType:
        return super().post(f"{self.resource}/{card_id}/report-stolen")

    def report_lost(self, card_id: str) -> ReturnType:
        return super().post(f"{self.resource}/{card_id}/report-lost")

    def close(self, card_id: str) -> ReturnType:
        return super().post(f"{self.resource}/{card_id}/close")

    def freeze(self, card_id: str) -> ReturnType:
        return super().post(f"{self.resource}/{card_id}/freeze")

    def unfreeze(self, card_id: str) -> ReturnType:
        return super().post(f"{self.resource}/{card_id}/unfreeze")

    def replace(self, card_id: str, shipping_address: Optional[Address]) -> ReturnType:
        request = ReplaceCardRequest(shipping_address)
        payload = request.to_json_api()
        return super().post(f"{self.resource}/{card_id}/replace", payload)

    def update(self, request: PatchCardRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().patch(f"{self.resource}/{request.card_id}", payload)

    def get(self, card_id: str, include: Optional[str] = "") -> ReturnType:
        return super().get(f"{self.resource}/{card_id}", {"include": include})

    def list(self, params: ListCardParams = None) -> Union[UnitResponse[List[Card]], UnitError]:
        params = params or ListCardParams()
        return super().get(self.resource, params.to_dict(), return_type=List[Card])

    def get_pin_status(self, card_id: str) -> Union[UnitResponse[PinStatusDTO], UnitError]:
        return super().get(f"{self.resource}/{card_id}/secure-data/pin/status", return_type=PinStatusDTO)

    def limits(self, card_id: str) -> Union[UnitResponse[CardLimitsDTO], UnitError]:
        return super().get(f"{self.resource}/{card_id}/limits", return_type=CardLimitsDTO)
