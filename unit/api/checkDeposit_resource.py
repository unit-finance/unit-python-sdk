from unit.utils.configuration import Configuration
from unit.api.base_resource import BaseResource
from unit.models.check_deposit import *
from unit.models.codecs import DtoDecoder


class CheckDepositResource(BaseResource):
    def __init__(self, configuration: Configuration):
        super().__init__("check-deposits", configuration)

    def create(self, request: CreateCheckDepositRequest) -> Union[UnitResponse[CheckDepositDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post_create(self.resource, payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CheckDepositDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, check_deposit_id: str, include: Optional[str] = None) -> Union[UnitResponse[CheckDepositDTO], UnitError]:
        params = {}

        if include:
            params["include"] = include

        response = super().get(f"{self.resource}/{check_deposit_id}", params)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[CheckDepositDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def get_image(self, check_deposit_id: str, is_back_side: Optional[bool] = False) -> Union[
        UnitResponse[bytes], UnitError]:
        params = {}
        response = super().get(f"{self.resource}/{check_deposit_id}/{'back' if is_back_side else 'front'}", params)
        if response.status_code == 200:
            return UnitResponse[bytes](response.content, None)
        else:
            return UnitError.from_json_api(response.json())
    def list(self, params: ListCheckDepositParams = None) -> Union[UnitResponse[List[CheckDepositDTO]], UnitError]:
        params = params or ListCheckDepositParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[CheckDepositDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def update(self, request: PatchCheckDepositRequest) -> Union[UnitResponse[CheckDepositDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"{self.resource}/{request.check_deposit_id}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CheckDepositDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def upload(self, request: UploadCheckDepositDocumentRequest) -> Union[UnitResponse[CheckDepositDTO], UnitError]:
        url = f"{self.resource}/{request.check_deposit_id}/{request.side}"

        headers = {"Content-Type": "image/jpeg"}

        response = super().put(url, request.file, headers)
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[CheckDepositDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def confirm(self, check_deposit_id: str) -> Union[UnitResponse[CheckDepositDTO], UnitError]:
        response = super().post(f"{self.resource}/{check_deposit_id}/confirm")

        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CheckDepositDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
