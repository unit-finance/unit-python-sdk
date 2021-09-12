from api.base_resource import BaseResource
from models.card import *
from models.codecs import DtoDecoder


class CardResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "cards"

    def create(self, request: CreateCardRequest) -> Union[UnitResponse[Card], UnitError]:
        payload = request.to_json_api()
        response = super().post(self.resource, payload)
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[Card](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def report_stolen(self, card_id: str) -> Union[UnitResponse[Card], UnitError]:
        response = super().post(f"{self.resource}/{card_id}/report-stolen")
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[Card](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def report_lost(self, card_id: str) -> Union[UnitResponse[Card], UnitError]:
        response = super().post(f"{self.resource}/{card_id}/report-lost")
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[Card](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def close_card(self, card_id: str) -> Union[UnitResponse[Card], UnitError]:
        response = super().post(f"{self.resource}/{card_id}/close")
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[Card](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def freeze_card(self, card_id: str) -> Union[UnitResponse[Card], UnitError]:
        response = super().post(f"{self.resource}/{card_id}/freeze")
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[Card](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def unfreeze_card(self, card_id: str) -> Union[UnitResponse[Card], UnitError]:
        response = super().post(f"{self.resource}/{card_id}/unfreeze")
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[Card](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def replace_card(self, card_id: str, shipping_address: Optional[str]) -> Union[UnitResponse[Union[IndividualDebitCardDTO, BusinessDebitCardDTO]], UnitError]:
        response = super().post(f"{self.resource}/{card_id}/replace")
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[Union[IndividualDebitCardDTO, BusinessDebitCardDTO]](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def update(self, request: PatchCardRequest) -> Union[UnitResponse[Card], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.card_id}", payload)
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[Card](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, card_id: str, include: Optional[str] = "") -> Union[UnitResponse[Card], UnitError]:
        response = super().get(f"{self.resource}/{card_id}")
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[Card](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, offset: int = 0, limit: int = 100) -> Union[UnitResponse[list[Card]], UnitError]:
        response = super().get(self.resource, {"page[limit]": limit, "page[offset]": offset})
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[Card](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
