from unit.api.base_resource import BaseResource
from unit.models.dispute import *
from unit.models.codecs import DtoDecoder


class DisputeResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "disputes"

    def get(self, dispute_id: str) -> Union[UnitResponse[DisputeDTO], UnitError]:
        response = super().get(f"{self.resource}/{dispute_id}")
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[DisputeDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListDisputeParams = None) -> Union[UnitResponse[List[DisputeDTO]], UnitError]:
        params = params or ListDisputeParams()
        response = super().get(self.resource, params.to_dict())
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[DisputeDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())


