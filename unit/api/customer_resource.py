from unit.utils.configuration import Configuration
from unit.api.base_resource import BaseResource
from unit.models.customer import *
from unit.models.codecs import DtoDecoder


class CustomerResource(BaseResource):
    def __init__(self, configuration: Configuration):
        super().__init__("customers", configuration)

    def update(self, request: PatchCustomerRequest) -> Union[UnitResponse[CustomerDTO], UnitError]:
        payload = request.to_json_api()
        response = super().patch(f"{self.resource}/{request.customer_id}", payload)

        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CustomerDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, customer_id: str) -> Union[UnitResponse[CustomerDTO], UnitError]:
        response = super().get(f"{self.resource}/{customer_id}")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CustomerDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: ListCustomerParams = None) -> Union[UnitResponse[List[CustomerDTO]], UnitError]:
        params = params or ListCustomerParams()
        response = super().get(self.resource, params.to_dict())
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            meta = response.json().get("meta")
            return UnitResponse[CustomerDTO](DtoDecoder.decode(data), meta=meta)
        else:
            return UnitError.from_json_api(response.json())

    def archive(self, request: ArchiveCustomerRequest) -> Union[UnitResponse[CustomerDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.customer_id}/archive", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CustomerDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def add_authorized_users(self, request: AddAuthorizedUsersRequest) -> Union[UnitResponse[CustomerDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(f"{self.resource}/{request.customer_id}/authorized-users", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CustomerDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def remove_authorized_users(self, request: RemoveAuthorizedUsersRequest) -> Union[UnitResponse[CustomerDTO], UnitError]:
        payload = request.to_json_api()
        response = super().delete(f"{self.resource}/{request.customer_id}/authorized-users", payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[CustomerDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

