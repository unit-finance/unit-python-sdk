from unit.api.base_resource import BaseResource
from unit.models.event import *
from unit.models.unit_objects import UnitResponse


class EventResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=EventDTO)
        self.resource = "events"

    def get(self, event_id: str) -> Union[UnitResponse[EventDTO], UnitError]:
        return super().get(f"{self.resource}/{event_id}")

    def list(self, params: ListEventParams = None) -> Union[UnitResponse[List[EventDTO]], UnitError]:
        params = params or ListEventParams()
        return super().get(self.resource, params.to_dict(), return_type=List[EventDTO])

    def fire(self, event_id: str) -> Union[UnitResponse, UnitError]:
        return super().post(f"{self.resource}/{event_id}", return_type=List)
