from unit.api.base_resource import BaseResource
from unit.models.account_end_of_day import *
from unit.models.codecs import DtoDecoder


class AccountEndOfDayResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "account-end-of-day"

    def list(self, params: AccountEndOfDayListParams = AccountEndOfDayListParams()) -> Union[UnitResponse[List[AccountEndOfDayDTO]], UnitError]:
        parameters = {"page[limit]": params.limit, "page[offset]": params.offset}

        if params.account_id != "":
            parameters |= {"filter[accountId]": params.account_id}

        if params.customer_id != "":
            parameters |= {"filter[customerId]": params.customer_id}

        if params.since != "":
            parameters |= {"filter[since]": params.since}

        if params.until != "":
            parameters |= {"filter[until]": params.until}

        response = super().get(self.resource, parameters)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[AccountEndOfDayDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

