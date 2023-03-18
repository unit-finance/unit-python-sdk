from unit.api.base_resource import BaseResource
from unit.models.application import *
from unit.models.codecs import DtoDecoder


class ApplicationResource(BaseResource):
    def __init__(self, api_url, token, retries):
        super().__init__(api_url, token, retries)
        self.resource = "applications"

    def create(self, request: Union[CreateIndividualApplicationRequest, CreateBusinessApplicationRequest]) -> Union[UnitResponse[ApplicationDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post_create(self.resource, payload)

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

    def update(self, request: PatchApplicationRequest) -> Union[UnitResponse[ApplicationDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"{self.resource}/{request.application_id}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[ApplicationDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list_documents(self, application_id: str) -> Union[UnitResponse[List[ApplicationDocumentDTO]], UnitError]:
        response = super().get(f"{self.resource}/{application_id}/documents")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[ApplicationDocumentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def create_document(self, application_id: str) -> Union[UnitResponse[ApplicationDocumentDTO], UnitError]:
        response = super().post(f"{self.resource}/{application_id}/documents/")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[ApplicationDocumentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def verify_document(self, request: VerifyDocumentRequest) -> Union[UnitResponse[ApplicationDocumentDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.application_id}/documents/{request.document_id}/verify",
                                payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[ApplicationDocumentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def download_document(self,  application_id: str, document_id: str, is_back_side: bool = False):
        url = f"{self.resource}/{application_id}/documents/{document_id}"
        if is_back_side:
            url += "/back"

        response = super().get(url)
        if super().is_20x(response.status_code):
            UnitResponse[str](response.text, None)
        else:
            return UnitError.from_json_api(response.json())

