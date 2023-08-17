from unit.api.base_resource import BaseResource
from unit.models.batch_release import *
from unit.models.codecs import DtoDecoder


class BatchReleaseResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = 'batch-releases'

    def create(self, batch_releases: List[CreateBatchRelease]) -> Union[UnitResponse[List[BatchReleaseDTO]], UnitError]:
        response = super().post(self.resource, {"data": batch_releases})
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[BatchReleaseDTO](DtoDecoder.decode(data), DtoDecoder.decode(data)) # is this right based on list??
        else:
            return UnitError.from_json_api(response.json())
