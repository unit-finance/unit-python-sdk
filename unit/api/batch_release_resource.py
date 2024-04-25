from unit.utils.configuration import Configuration
from unit.api.base_resource import BaseResource
from unit.models.batch_release import *
from unit.models.codecs import DtoDecoder


class BatchReleaseResource(BaseResource):
    def __init__(self, configuration: Configuration):
        super().__init__('batch-releases', configuration)

    def create(self, batch_releases: List[BatchReleaseDTO]) -> Union[UnitResponse[List[BatchReleaseDTO]], UnitError]:
        response = super().post(self.resource, {"data": batch_releases})
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[List[BatchReleaseDTO]](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())