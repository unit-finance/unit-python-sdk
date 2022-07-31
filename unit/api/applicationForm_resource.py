from unit.api.base_resource import BaseResource
from unit.models.applicationForm import *
from unit.models.unit_objects import UnitResponse


ReturnType = Union[UnitResponse[ApplicationFormDTO], UnitError]


class ApplicationFormResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token, return_type=ApplicationFormDTO)
        self.resource = "application-forms"

    def create(self, request: CreateApplicationFormRequest) -> ReturnType:
        payload = request.to_json_api()
        return super().post(self.resource, payload)

    def get(self, application_form_id: str, include: Optional[str] = "") -> ReturnType:
        return super().get(f"{self.resource}/{application_form_id}", {"include": include})

    def list(self, params: ListApplicationFormParams = None) -> Union[UnitResponse[List[ApplicationFormDTO]], UnitError]:
        params = params or ListApplicationFormParams()
        return super().get(self.resource, params.to_dict(), return_type=List[ApplicationFormDTO])

