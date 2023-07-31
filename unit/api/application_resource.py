from unit.utils.configuration import Configuration
from unit.api.base_resource import BaseResource
from unit.models.application import *
from unit.models.codecs import DtoDecoder


class ApplicationResource(BaseResource):
    def __init__(self, configuration: Configuration):
        super().__init__("applications", configuration)

    def create(self, request: CreateApplicationRequest) -> Union[UnitResponse[ApplicationDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post_create(self.resource, payload)

        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[ApplicationDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListApplicationParams = None) -> Union[UnitResponse[List[ApplicationDTO]], UnitError]:
        params = params or ListApplicationParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            meta = response.json().get("meta")
            return UnitResponse[ApplicationDTO](DtoDecoder.decode(data), meta=meta)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, application_id: str) -> Union[UnitResponse[ApplicationDTO], UnitError]:
        response = super().get(f"{self.resource}/{application_id}")
        if super().is_20x(response.status_code):
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
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[ApplicationDocumentDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def update(self, request: UnionPatchApplicationRequest) -> Union[UnitResponse[ApplicationDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"{self.resource}/{request.application_id}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[ApplicationDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def update_business_beneficial_owner(self, request: PatchBusinessBeneficialOwnerRequest) -> Union[UnitResponse[BeneficialOwnerDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"beneficial-owner/{request.beneficial_owner_id}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[BeneficialOwnerDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def cancel(self, request: CancelApplicationRequest) -> Union[UnitResponse[ApplicationDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.application_id}/cancel", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[ApplicationDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())
