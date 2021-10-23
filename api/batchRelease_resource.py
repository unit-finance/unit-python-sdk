from api.base_resource import BaseResource
from models.batchRelease import *
from models.codecs import DtoDecoder


class BatchReleaseResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "batch-releases"

    def create(self, request: [CreateBatchReleaseRequest]) -> Union[UnitResponse[BatchReleaseDTO], UnitError]:
        payload = {"data": list(map(lambda r: r.to_json_api(), request))}
        response = super().post(self.resource, payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[BatchReleaseDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
