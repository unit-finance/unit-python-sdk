from unit.api.base_resource import BaseResource
from unit.models.application import *
from unit.models.unit_objects import UnitResponse

ReturnType = Union[UnitResponse[ApplicationDTO], UnitError]


class ApplicationResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=ApplicationDocumentDTO)
        self.resource = "applications"

    def create(self, request: Union[CreateIndividualApplicationRequest, CreateBusinessApplicationRequest]) -> ReturnType:
        payload = request.to_json_api()
        return super().post(self.resource, payload)

    def list(self, params: ListApplicationParams = None) -> Union[UnitResponse[List[ApplicationDTO]], UnitError]:
        params = params or ListApplicationParams()
        return super().get(self.resource, params.to_dict(), return_type=List[ApplicationDTO])

    def get(self, application_id: str) -> ReturnType:
        return super().get(f"{self.resource}/{application_id}")

    def upload(self, request: UploadDocumentRequest):
        url = f"{self.resource}/{request.application_id}/documents/{request.document_id}"
        if request.is_back_side:
            url += "/back"

        return super().put(url, request.file, request.to_dict())

    def update(self, request: PatchApplicationRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().patch(f"{self.resource}/{request.application_id}", payload)

