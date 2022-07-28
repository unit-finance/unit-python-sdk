from unit.api.base_resource import BaseResource
from unit.models.event import *
from unit.models.codecs import DtoDecoder


class EventResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "events"

    def get(self, event_id: str) -> Union[UnitResponse[EventDTO], UnitError]:
        response = super().get(f"{self.resource}/{event_id}")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[EventDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListEventParams = None) -> Union[UnitResponse[List[EventDTO]], UnitError]:
        params = params or ListEventParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[EventDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def fire(self, event_id: str) -> Union[UnitResponse, UnitError]:
        response = super().post(f"{self.resource}/{event_id}")
        if super().is_20x(response.status_code):
            return UnitResponse([], None)
        else:
            return UnitError.from_json_api(response.json())
