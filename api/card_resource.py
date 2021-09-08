from api.base_resource import BaseResource
from models.card import *
from models.codecs import DtoDecoder


class CardResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "cards"

    def get(self, card_id: str, include: Optional[str] = "") -> Union[UnitResponse[Card], UnitError]:
        response = super().get(f"{self.resource}/{card_id}")
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[Card](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
