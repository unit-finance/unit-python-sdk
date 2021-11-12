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

    def list(self, offset: int = 0, limit: int = 100) -> Union[UnitResponse[list[ApplicationDTO]], UnitError]:
        response = super().get(self.resource, {"page[limit]": limit, "page[offset]": offset})
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[ApplicationDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list_documents(self, application_id: str):
        response = super().get(f"{self.resource}/{application_id}/documents", None)
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[ApplicationDocumentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def upload(self, request: UploadDocumentRequest):
        url = f"{self.resource}/{request.application_id}/documents/{request.document_id}"
        if request.is_back_side:
            url += "/back"

        headers = {}
        #
        # match request.fileType:
        #     case "jpeg":
        #         headers = {"Content-Type": "image/jpeg"}
        #     case "png":
        #         headers = {"Content-Type": "image/png"}
        #     case "pdf":
        #         headers = {"Content-Type": "image/pdf"}
        #     case _:
        #         headers = {}

        response = super().put(url, request.file, headers)
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[ApplicationDocumentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, application_id: str)-> Union[UnitResponse[ApplicationDTO], UnitError]:
        response = super().get(f"{self.resource}/{application_id}")
        if response.status_code == 200:
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[ApplicationDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

