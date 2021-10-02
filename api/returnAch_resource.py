from api.base_resource import BaseResource
from models.transaction import ReturnedReceivedAchTransactionDTO
from models.returnAch import *
from models.codecs import DtoDecoder


class ReturnAchResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "returns"

    def return_ach(self, request: ReturnReceivedAchTransactionRequest) -> Union[UnitResponse[ReturnedReceivedAchTransactionDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.transaction_id}", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[ReturnedReceivedAchTransactionDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

