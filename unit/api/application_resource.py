from unit.api.base_resource import BaseResource
from unit.models.application import *
from unit.models.codecs import DtoDecoder


class ApplicationResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "applications"

    def create(self, request: Union[CreateIndividualApplicationRequest, CreateBusinessApplicationRequest]) -> Union[UnitResponse[ApplicationDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(self.resource, payload)

        if response.ok:
            data = response.json().get("data")
            included = response.json().get("included")
            if data["type"] == "individualApplication":
                return UnitResponse[IndividualApplicationDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
            else:
                return UnitResponse[BusinessApplicationDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListApplicationParams = None) -> Union[UnitResponse[List[ApplicationDTO]], UnitError]:
        params = params or ListApplicationParams()
        response = super().get(self.resource, params.to_dict())
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[ApplicationDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, application_id: str) -> Union[UnitResponse[ApplicationDTO], UnitError]:
        response = super().get(f"{self.resource}/{application_id}")
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[ApplicationDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
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
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[ApplicationDocumentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
