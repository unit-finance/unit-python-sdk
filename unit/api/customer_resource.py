from unit.api.base_resource import BaseResource
from unit.models.customer import *
from unit.models.unit_objects import UnitResponse

ReturnType = Union[UnitResponse[CustomerDTO], UnitError]
PatchCustomerRequest = Union[UnitResponse[CustomerDTO], UnitError]


class CustomerResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=CustomerDTO)
        self.resource = "customers"

    def update(self, request: PatchCustomerRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().patch(f"{self.resource}/{request.customer_id}", payload)

    def get(self, customer_id: str) -> ReturnType:
        return super().get(f"{self.resource}/{customer_id}")

    def list(self, params: ListCustomerParams = None) -> Union[UnitResponse[List[CustomerDTO]], UnitError]:
        params = params or ListCustomerParams()
        return super().get(self.resource, params.to_dict(), return_type=List[CustomerDTO])

    def archive(self, request: ArchiveCustomerRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().post(f"{self.resource}/{request.customer_id}/archive", payload)
