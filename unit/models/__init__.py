import json
from typing import TypeVar, Generic, Union, Optional, Literal, List, Dict
from datetime import datetime, date


def to_camel_case(snake_str):
    components = snake_str.lstrip('_').split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


class UnitDTO(object):
    def to_dict(self):
        if type(self) is dict:
            return self
        else:
            v = vars(self)
            return dict((to_camel_case(k), val) for k, val in v.items() if val is not None)


class Relationship(UnitDTO):
    def __init__(self, _type: str, _id: str):
        self.type = _type
        self.id = _id

    def to_dict(self, nested: Optional[bool] = True):
        if nested:
            return {"data": {"type": self.type, "id": self.id}}
        else:
            return {"type": self.type, "id": self.id}


T = TypeVar('T')


class RelationshipArray(Generic[T], UnitDTO):
    def __init__(self, l: List[T]):
        self.relationships = l

    def to_dict(self):
        return {"data": list(map(lambda r: r.to_dict(False), self.relationships))}


class UnitResponse(Generic[T]):
    def __init__(self, data: Union[T, List[T]], included):
        self.data = data
        self.included = included

    @staticmethod
    def from_json_api(data: str):
        pass


class UnitRequest(object):
    def to_json_api(self) -> Dict:
        pass


class UnitParams(object):
    def to_dict(self) -> Dict:
        pass


class RawUnitObject(UnitDTO):
    def __init__(self, _id, _type, attributes, relationships):
        self.id = _id
        self.type = _type
        self.attributes = attributes
        self.relationships = relationships

    def to_dict(self):
        v = vars(self.attributes)
        return dict((to_camel_case(k), val) for k, val in v.items() if val is not None)


class UnitErrorPayload(object):
    def __init__(self, title: str, status: str, detail: Optional[str] = None, details: Optional[str] = None,
                 source: Optional[Dict] = None, code: Optional[str] = None):
        self.title = title
        self.status = status
        self.detail = detail
        self.details = details
        self.source = source
        self.code = code

    def __str__(self):
        return self.detail


class UnitError(object):
    def __init__(self, errors: List[UnitErrorPayload]):
        self.errors = errors

    @staticmethod
    def from_json_api(data: Dict):
        errors = []
        for err in data["errors"]:
            errors.append(
                UnitErrorPayload(err.get("title"), err.get("status"), err.get("detail", None),
                                 err.get("details", None), err.get("source", None), err.get("code", None))
            )

        return UnitError(errors)

    def __str__(self):
        return json.dumps({"errors": [{"title": err.title, "status": err.status, "detail": err.detail,
                                "details": err.details, "source": err.source, "code": err.code} for err in self.errors]})


Status = Literal["Approved", "Denied", "PendingReview"]
Title = Literal["CEO", "COO", "CFO", "President"]
EntityType = Literal["Corporation", "LLC", "Partnership"]


class FullName(UnitDTO):
    def __init__(self, first: str, last: str):
        self.first = first
        self.last = last

    @staticmethod
    def from_json_api(data: Dict):
        return FullName(data.get("first"), data.get("last"))


# todo: Alex - use typing.Literal for multi accepted values (e.g country)
class Address(UnitDTO):
    def __init__(self, street: str, city: str, state: str, postal_code: str, country: str,
                 street2: Optional[str] = None):
        self.street = street
        self.street2 = street2
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country

    @staticmethod
    def from_json_api(data: Dict):
        return Address(data.get("street"), data.get("city"), data.get("state"),
                data.get("postalCode"), data.get("country"), data.get("street2", None))


class Phone(UnitDTO):
    def __init__(self, country_code: str, number: str):
        self.country_code = country_code
        self.number = number

    @staticmethod
    def from_json_api(data: Dict):
        return Phone(data.get("countryCode"), data.get("number"))


class BusinessContact(UnitDTO):
    def __init__(self, full_name: FullName, email: str, phone: Phone):
        self.full_name = full_name
        self.email = email
        self.phone = phone

    @staticmethod
    def from_json_api(data: Dict):
        return BusinessContact(FullName.from_json_api(data.get("fullName")), data.get("email"), Phone.from_json_api(data.get("phone")))


class Officer(UnitDTO):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 status: Optional[Status] = None, title: Optional[Title] = None, ssn: Optional[str] = None,
                 passport: Optional[str] = None, nationality: Optional[str] = None):
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone = phone
        self.email = email
        self.status = status
        self.title = title
        self.ssn = ssn
        self.passport = passport
        self.nationality = nationality

    @staticmethod
    def from_json_api(data: Dict):
        return Officer(data.get("fullName"), data.get("dateOfBirth"), data.get("address"), data.get("phone"),
                data.get("email"), data.get("status"), data.get("title"), data.get("ssn"), data.get("passport"),
                data.get("nationality"))


class BeneficialOwner(UnitDTO):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 status: Optional[Status] = None, ssn: Optional[str] = None, passport: Optional[str] = None,
                 nationality: Optional[str] = None, percentage: Optional[int] = None):
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone = phone
        self.email = email
        self.status = status
        self.ssn = ssn
        self.passport = passport
        self.nationality = nationality
        self.percentage = percentage

    @staticmethod
    def from_json_api(l: List):
        beneficial_owners = []
        for data in l:
            beneficial_owners.append(BeneficialOwner(data.get("fullName"), data.get("dateOfBirth"), data.get("address"),
                data.get("phone"), data.get("email"), data.get("status"), data.get("ssn"),
                data.get("passport"), data.get("nationality"), data.get("percentage")))
        return beneficial_owners


class AuthorizedUser(UnitDTO):
    def __init__(self, full_name: FullName, email: str, phone: Phone, jwt_subject: Optional[str]):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.jwt_subject = jwt_subject

    @staticmethod
    def from_json_api(data):
        if data is None:
            return None

        if data is []:
            return []

        if type(data) is dict:
            return AuthorizedUser(FullName.from_json_api(data.get("fullName")), data.get("email"),
                              Phone.from_json_api(data.get("phone")), data.get("jwtSubject"))

        return [AuthorizedUser(FullName.from_json_api(d.get("fullName")), d.get("email"),
                              Phone.from_json_api(d.get("phone")), d.get("jwtSubject")) for d in data]

class WireCounterparty(UnitDTO):
    def __init__(self, routing_number: str, account_number: str, name: str, address: Address):
        self.routing_number = routing_number
        self.account_number = account_number
        self.name = name
        self.address = address

    @staticmethod
    def from_json_api(data: Dict):
        return WireCounterparty(data["routingNumber"], data["accountNumber"], data["name"],
                                Address.from_json_api(data["address"]))

class Counterparty(UnitDTO):
    def __init__(self, routing_number: str, account_number: str, account_type: str, name: str):
        self.routing_number = routing_number
        self.account_number = account_number
        self.account_type = account_type
        self.name = name

    @staticmethod
    def from_json_api(data: Dict):
        return Counterparty(data["routingNumber"], data["accountNumber"], data["accountType"], data["name"])

class Coordinates(UnitDTO):
    def __init__(self, longitude: float, latitude: float):
        self.longitude = longitude
        self.latitude = latitude

    @staticmethod
    def from_json_api(data: Dict):
        if not data:
            return None

        return Coordinates(data["longitude"], data["latitude"])


class Merchant(UnitDTO):
    def __init__(self, name: str, type: int, category: str, location: Optional[str]):
        self.name = name
        self.type = type
        self.category = category
        self.location = location

    @staticmethod
    def from_json_api(data: Dict):
        return Merchant(data["name"], data["type"], data["category"], data.get("location"))

class CardLevelLimits(UnitDTO):
    def __init__(self, daily_withdrawal: int, daily_purchase: int, monthly_withdrawal: int, monthly_purchase: int):
        self.daily_withdrawal = daily_withdrawal
        self.daily_purchase = daily_purchase
        self.monthly_withdrawal = monthly_withdrawal
        self.monthly_purchase = monthly_purchase

    @staticmethod
    def from_json_api(data: Dict):
        return CardLevelLimits(data["dailyWithdrawal"], data["dailyPurchase"], data["monthlyWithdrawal"],
                      data["monthlyPurchase"])

class CardTotals(UnitDTO):
    def __init__(self, withdrawals: int, deposits: int, purchases: int):
        self.withdrawals = withdrawals
        self.deposits = deposits
        self.purchases = purchases

    @staticmethod
    def from_json_api(data: Dict):
        return CardTotals(data["withdrawals"], data["deposits"], data["purchases"])


class DeviceFingerprint(UnitDTO):
    def __init__(self, value: str, provider: str = "iovation"):
        self.value = value
        self.provider = provider

    def to_json_api(self):
        return {
            "value": self.value,
            "provider": self.provider,
        }

    @classmethod
    def from_json_api(cls, data: Dict):
        return cls(value=data["value"], provider=data["provider"])

class CheckCounterparty(object):
    def __init__(self, routing_number: str, account_number: str, name: str):
        self.routing_number = routing_number
        self.account_number = account_number
        self.name = name

    @staticmethod
    def from_json_api(data: Dict):
        if not data:
            return None

        return CheckCounterparty(data["routingNumber"], data["accountNumber"], data["name"])