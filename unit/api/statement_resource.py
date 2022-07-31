from unit.api.base_resource import BaseResource
from unit.models.statement import *
from unit.models.unit_objects import UnitResponse


class StatementResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=str)
        self.resource = "statements"

    def get(self, params: GetStatementParams) -> Union[UnitResponse[str], UnitError]:
        parameters = {"language": params.language}
        if params.customer_id:
            parameters["filter[customerId]"] = params.customer_id

        return super().get(f"{self.resource}/{params.statement_id}/{params.output_type}", parameters, as_text=True)

    def get_bank_verification(self, account_id: str, include_proof_of_funds: Optional[bool] = False) ->\
            Union[UnitResponse[str], UnitError]:
        return super().get(f"{self.resource}/{account_id}/bank/pdf", {"includeProofOfFunds": include_proof_of_funds},
                           as_text=True)

    def list(self, params: ListStatementParams = None) -> Union[UnitResponse[List[StatementDTO]], UnitError]:
        params = params or ListStatementParams()
        return super().get(self.resource, params.to_dict(), return_type=List[StatementDTO])
