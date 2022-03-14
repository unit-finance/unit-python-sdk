from unit.api.base_resource import BaseResource
from unit.models.statement import *
from unit.models.codecs import DtoDecoder


class StatementResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "statements"

    def get(self, params: GetStatementParams) -> Union[UnitResponse[str], UnitError]:
        parameters = {"language": params.language}
        if params.customer_id:
            parameters["filter[customerId]"] = params.customer_id

        response = super().get(f"{self.resource}/{params.statement_id}/{params.output_type}", parameters)
        if response.status_code == 200:
            return UnitResponse[str](response.text, None)
        else:
            return UnitError.from_json_api(response.json())

    def get_bank_verification(self, account_id: str, include_proof_of_funds: Optional[bool] = False) -> Union[UnitResponse[str], UnitError]:
        response = super().get(f"{self.resource}/{account_id}/bank/pdf",
                               {"includeProofOfFunds": include_proof_of_funds})
        if response.status_code == 200:
            return UnitResponse[str](response.text, None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListStatementParams = None) -> Union[UnitResponse[List[StatementDTO]], UnitError]:
        params = params or ListStatementParams()
        response = super().get(self.resource, params.to_dict())
        if response.status_code == 200:
            data = response.json().get("data")
            return UnitResponse[StatementDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

