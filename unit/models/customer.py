from unit.utils import date_utils
from unit.models import *


class IndividualCustomerDTO(object):
    def __init__(self, id: str, created_at: datetime, full_name: FullName, date_of_birth: date, address: Address,
                 phone: Phone, email: str, ssn: Optional[str], passport: Optional[str], nationality: Optional[str],
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = 'individualCustomer'
        self.attributes = {"createdAt": created_at, "fullName": full_name, "dateOfBirth": date_of_birth,
                           "address": address, "phone": phone, "email": email, "ssn": ssn, "passport": passport,
                           "nationality": nationality, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return IndividualCustomerDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]),
            FullName.from_json_api(attributes["fullName"]), date_utils.to_date(attributes["dateOfBirth"]),
            Address.from_json_api(attributes["address"]), Phone.from_json_api(attributes["phone"]),
            attributes["email"], attributes.get("ssn"), attributes.get("passport"), attributes.get("nationality"),
            attributes.get("tags"), relationships
        )


class BusinessCustomerDTO(object):
    def __init__(self, id: str, created_at: datetime, name: str, address: Address, phone: Phone,
                 state_of_incorporation: str, ein: str, entity_type: EntityType, contact: BusinessContact,
                 authorized_users: [AuthorizedUser], dba: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = 'businessCustomer'
        self.attributes = {"createdAt": created_at, "name": name, "address": address, "phone": phone,
                           "stateOfIncorporation": state_of_incorporation, "ein": ein, "entityType": entity_type,
                           "contact": contact, "authorizedUsers": authorized_users, "dba": dba, "tags": tags}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessCustomerDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["name"],
            Address.from_json_api(attributes["address"]), Phone.from_json_api(attributes["phone"]),
            attributes["stateOfIncorporation"], attributes["ein"], attributes["entityType"],
            BusinessContact.from_json_api(attributes["contact"]),
            [AuthorizedUser.from_json_api(user) for user in attributes["authorizedUsers"]],
            attributes.get("dba"), attributes.get("tags"), relationships)

CustomerDTO = Union[IndividualCustomerDTO, BusinessCustomerDTO]


class PatchIndividualCustomerRequest(UnitRequest):
    def __init__(self, customer_id: str, address: Optional[Address] = None, phone: Optional[Phone] = None,
                 email: Optional[str] = None, dba: Optional[str] = None, tags: Optional[Dict[str, str]] = None):
        self.customer_id = customer_id
        self.address = address
        self.phone = phone
        self.email = email
        self.dba = dba
        self.tags = tags

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

