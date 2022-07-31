from unit.api.base_resource import BaseResource
from unit.models.check_deposit import *
from unit.models.unit_objects import UnitResponse

ReturnType = Union[UnitResponse[CheckDepositDTO], UnitError]


class CheckDepositResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=CheckDepositDTO)
        self.resource = "check-deposits"

    def create(self, request: CreateCheckDepositRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().post(self.resource, payload)

    def get(self, check_deposit_id: str, include: Optional[str] = None) -> ReturnType:
        params = {}
        if include:
            params["include"] = include
        return super().get(f"{self.resource}/{check_deposit_id}", params)

    def list(self, params: ListCheckDepositParams = None) -> Union[UnitResponse[List[CheckDepositDTO]], UnitError]:
        params = params or ListCheckDepositParams()
        return super().get(self.resource, params.to_dict(), return_type=List[CheckDepositDTO])

    def update(self, request: PatchCheckDepositRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().patch(f"{self.resource}/{request.check_deposit_id}", payload)

    def upload(self, request: UploadCheckDepositDocumentRequest):
        url = f"{self.resource}/{request.check_deposit_id}/{request.side}"
        headers = {"Content-Type": "image/jpeg"}
        return super().put(url, request.file, headers)


