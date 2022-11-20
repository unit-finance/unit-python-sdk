from typing import Union

from unit.api.base_resource import BaseResource
from unit.models.application import *
from unit.models.unit_models import UnitResponse


class ApplicationResource(BaseResource):
    def __init__(self, api_url, token, retries):
        super().__init__(api_url, token, retries)
        self.resource = "applications"

    def create(self, request: Union[CreateIndividualApplicationRequest, CreateBusinessApplicationRequest]) -> Union[UnitResponse[ApplicationDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post_create(self.resource, payload)

        if super().is_20x(response.status_code):
            return UnitResponse.from_json_api(response.json())
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListApplicationParams = None) -> Union[UnitResponse[List[ApplicationDTO]], UnitError]:
        params = params or ListApplicationParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            return UnitResponse.from_json_api(response.json())
        else:
            return UnitError.from_json_api(response.json())

    def get(self, application_id: str) -> Union[UnitResponse[ApplicationDTO], UnitError]:
        response = super().get(f"{self.resource}/{application_id}")
        if super().is_20x(response.status_code):
            return UnitResponse.from_json_api(response.json())
        else:
            return UnitError.from_json_api(response.json())

    def upload(self, request: UploadDocumentRequest):
        url = f"{self.resource}/{request.application_id}/documents/{request.document_id}"
        if request.is_back_side:
            url += "/back"

        headers = {}

        if request.file_type == "jpeg":
                headers = {"Content-Type": "image/jpeg"}
        if request.file_type == "png":
                headers = {"Content-Type": "image/png"}
        if request.file_type == "pdf":
                headers = {"Content-Type": "application/pdf"}

        response = super().put(url, request.file, headers)
        if super().is_20x(response.status_code):
            return UnitResponse.from_json_api(response.json())
        else:
            return UnitError.from_json_api(response.json())

    def update(self, request: PatchApplicationRequest) -> Union[UnitResponse[ApplicationDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"{self.resource}/{request.application_id}", payload)
        if super().is_20x(response.status_code):
            return UnitResponse.from_json_api(response.json())
        else:
            return UnitError.from_json_api(response.json())

