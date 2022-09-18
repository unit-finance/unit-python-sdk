from unit.models import *

ArchiveReason = Literal["Inactive", "FraudACHActivity", "FraudCardActivity", "FraudCheckActivity",
                        "FraudApplicationHistory", "FraudAccountActivity", "FraudClientIdentified"]

CustomerStatus = Literal["Active", "Archived"]


class IndividualCustomerDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return IndividualCustomerDTO(_id, _type, attributes_to_object(attributes), relationships)


class BusinessCustomerDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessCustomerDTO(_id, _type, attributes_to_object(attributes), relationships)


CustomerDTO = Union[IndividualCustomerDTO, BusinessCustomerDTO]


class PatchIndividualCustomerRequest(UnitRequest):
    def __init__(self, customer_id: str, address: Optional[Address] = None, phone: Optional[Phone] = None,
                 email: Optional[str] = None, dba: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 jwt_subject: Optional[str] = None, authorized_users: Optional[AuthorizedUser] = None):
        self.customer_id = customer_id
        self.address = address
        self.phone = phone
        self.email = email
        self.dba = dba
        self.tags = tags
        self.jwt_subject = jwt_subject
        self.authorized_users = authorized_users

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "individualCustomer",
                "attributes": {}
            }
        }

        if self.address:
            payload["data"]["attributes"]["address"] = self.address

        if self.phone:
            payload["data"]["attributes"]["phone"] = self.phone

        if self.email:
            payload["data"]["attributes"]["email"] = self.email

        if self.dba:
            payload["data"]["attributes"]["dba"] = self.dba

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        if self.jwt_subject:
            payload["data"]["attributes"]["jwtSubject"] = self.jwt_subject

        if self.authorized_users:
            payload["data"]["attributes"]["authorizedUsers"] = self.authorized_users

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class PatchBusinessCustomerRequest(UnitRequest):
    def __init__(self, customer_id: str, address: Optional[Address] = None, phone: Optional[Phone] = None,
                 contact: Optional[BusinessContact] = None, authorized_users: Optional[List[AuthorizedUser]] = None,
                 tags: Optional[Dict[str, str]] = None):
        self.customer_id = customer_id
        self.address = address
        self.phone = phone
        self.contact = contact
        self.authorized_users = authorized_users
        self.tags = tags

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "businessCustomer",
                "attributes": {}
            }
        }

        if self.address:
            payload["data"]["attributes"]["address"] = self.address

        if self.phone:
            payload["data"]["attributes"]["phone"] = self.phone

        if self.contact:
            payload["data"]["attributes"]["contact"] = self.contact

        if self.authorized_users:
            payload["data"]["attributes"]["authorizedUsers"] = self.authorized_users

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class ListCustomerParams(UnitParams):
    def __init__(self, offset: int = 0, limit: int = 100, query: Optional[str] = None, email: Optional[str] = None,
                 tags: Optional[object] = None, sort: Optional[Literal["createdAt", "-createdAt"]] = None):
        self.offset = offset
        self.limit = limit
        self.query = query
        self.email = email
        self.tags = tags
        self.sort = sort

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.query:
            parameters["filter[query]"] = self.query
        if self.email:
            parameters["filter[email]"] = self.email
        if self.tags:
            parameters["filter[tags]"] = self.tags
        if self.sort:
            parameters["sort"] = self.sort
        return parameters


class ArchiveCustomerRequest(UnitRequest):
    def __init__(self, customer_id: str, reason: Optional[ArchiveReason] = None):
        self.customer_id = customer_id
        self.reason = reason

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "archiveCustomer",
                "attributes": {}
            }
        }

        if self.reason:
            payload["data"]["attributes"]["reason"] = self.reason

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())
