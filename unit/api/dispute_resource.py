from unit.api.base_resource import BaseResource
from unit.models.dispute import *
from unit.models.unit_objects import UnitResponse


class DisputeResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "disputes"

    def get(self, dispute_id: str) -> Union[UnitResponse[DisputeDTO], UnitError]:
        return super().get(f"{self.resource}/{dispute_id}", return_type=DisputeDTO)

    def list(self, params: ListDisputeParams = None) -> Union[UnitResponse[List[DisputeDTO]], UnitError]:
        params = params or ListDisputeParams()
        return super().get(self.resource, params.to_dict(), return_type=List[DisputeDTO])
