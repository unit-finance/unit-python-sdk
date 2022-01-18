from unit.api.base_resource import BaseResource
from unit.models.authorization import *
from unit.models.codecs import DtoDecoder


class AuthorizationResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "authorizations"

    def get(self, authorization_id: str, include_non_authorized: Optional[bool] = False) -> Union[UnitResponse[AuthorizationDTO], UnitError]:
        params = {"filter[includeNonAuthorized]": include_non_authorized}

        response = super().get(f"{self.resource}/{authorization_id}", params)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AuthorizationDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def list(self, params: AuthorizationListParams = AuthorizationListParams()) -> Union[UnitResponse[List[AuthorizationDTO]], UnitError]:
        parameters = {"page[limit]": params.limit, "page[offset]": params.offset}

        if params.account_id:
            parameters["filter[accountId]"] = params.account_id

        if params.customer_id:
            parameters["filter[customerId]"] = params.customer_id

        if params.card_id:
            parameters["filter[cardId]"] = params.card_id

        if params.since:
            parameters["filter[since]"] = params.since

        if params.until:
            parameters["filter[until]"] = params.until

        if params.include_non_authorized:
            parameters["filter[includeNonAuthorized]"] = params.include_non_authorized

        if params.status:
            parameters["filter[status]"] = params.status

        response = super().get(self.resource, parameters)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AuthorizationDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())
