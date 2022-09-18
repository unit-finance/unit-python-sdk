from unit.models import *
from unit.utils import date_utils

AuthorizationStatus = Literal["Authorized", "Completed", "Canceled", "Declined"]


class AuthorizationDTO(UnitDTO):
    def __init__(self, _id: str, _type: str, attributes: Dict[str, object], relationships: Dict[str, Relationship]):
        super().__init__(_id, _type, attributes, relationships)
        self.attributes["createdAt"] = date_utils.to_datetime(attributes["createdAt"])

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationDTO(_id, _type, attributes, relationships)


class ListAuthorizationParams(UnitParams):
    def __init__(self, limit: int = 100, offset: int = 0, account_id: Optional[str] = None,
                 customer_id: Optional[str] = None, card_id: Optional[str] = None, since: Optional[str] = None,
                 until: Optional[str] = None, include_non_authorized: Optional[bool] = False,
                 status: Optional[str] = None, sort: Optional[Literal["createdAt", "-createdAt"]] = None):
        self.limit = limit
        self.offset = offset
        self.account_id = account_id
        self.customer_id = customer_id
        self.card_id = card_id
        self.since = since
        self.until = until
        self.include_non_authorized = include_non_authorized
        self.status = status
        self.sort = sort

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.account_id:
            parameters["filter[accountId]"] = self.account_id
        if self.card_id:
            parameters["filter[cardId]"] = self.card_id
        if self.include_non_authorized:
            parameters["filter[includeNonAuthorized]"] = self.include_non_authorized
        if self.status:
            parameters["filter[status]"] = self.status
        if self.since:
            parameters["filter[since]"] = self.since
        if self.until:
            parameters["filter[until]"] = self.until
        if self.sort:
            parameters["sort"] = self.sort
        return parameters
