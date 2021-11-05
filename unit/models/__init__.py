import json
from typing import TypeVar, Generic, Union, Optional, Literal
from datetime import datetime, date


class Relationship(object):
    def __init__(self, _type: str, _id: str):
        self.type = _type
        self.id = _id

    def to_dict(self):
        return {"type": self.type, "id": self.id}


T = TypeVar('T')

class RelationshipArray(Generic[T]):
    def __init__(self, l: list[T]):
        self.relationships = l


class UnitResponse(Generic[T]):
    def __init__(self, data: Union[T, list[T]], included):
        self.data = data
        self.included = included

    @staticmethod
    def from_json_api(data: str):
        pass


class UnitRequest(object):
    def to_json_api(self) -> dict:
        pass


class UnitErrorPayload(object):
    def __init__(self, title: str, status: str, detail: Optional[str] = None, details: Optional[str] = None,
                 source: Optional[dict] = None):
        self.title = title
        self.status = status
        self.detail = detail
        self.details = details
        self.source = source

    def __str__(self):
        return self.detail


class UnitError(object):
    def __init__(self, errors: list[UnitErrorPayload]):
        self.errors = errors

    @staticmethod
    def from_json_api(data: dict):
        errors = []
        for err in data["errors"]:
            errors.append(
                UnitErrorPayload(err.get("title"), err.get("status"), err.get("detail", None),
                                 err.get("details", None), err.get("source", None))
            )

        return UnitError(errors)

    def __str__(self):
        return json.dumps({"errors": [{"title": err.title, "status": err.status, "detail": err.detail,
                                "details": err.details, "source": err.source} for err in self.errors]})


Status = Literal["Approved", "Denied", "PendingReview"]
Title = Literal["CEO", "COO", "CFO", "President"]
EntityType = Literal["Corporation", "LLC", "Partnership"]

class FullName(object):
    def __init__(self, first: str, last: str):
        self.first = first
        self.last = last

    @staticmethod
    def from_json_api(data: dict):
        FullName(data.get("first"), data.get("last"))


# todo: Alex - use typing.Literal for multi accepted values (e.g country)
class Address(object):
    def __init__(self, street: str, city: str, state: str, postal_code: str, country: str,
                 street2: Optional[str] = None):
        self.street = street
        self.street2 = street2
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country

    @staticmethod
    def from_json_api(data: dict):
        return Address(data.get("street"), data.get("city"), data.get("state"),
                data.get("postal_code"), data.get("country"), data.get("street2", None))


class Phone(object):
    def __init__(self, country_code: str, number: str):
        self.country_code = country_code
        self.number = number

    @staticmethod
    def from_json_api(data: dict):
        return Phone(data.get("countryCode"), data.get("number"))


class BusinessContact(object):
    def __init__(self, full_name: FullName, email: str, phone: Phone):
        self.full_name = full_name
        self.email = email
        self.phone = phone

    @staticmethod
    def from_json_api(data: dict):
        return BusinessContact(data.get("fullName"), data.get("email"), data.get("phone"))


class Officer(object):
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
    def from_json_api(data: dict):
        return Officer(data.get("fullName"), data.get("dateOfBirth"), data.get("address"), data.get("phone"),
                data.get("email"), data.get("status"), data.get("title"), data.get("ssn"), data.get("passport"),
                data.get("nationality"))


class BeneficialOwner(object):
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
    def from_json_api(l: list):
        beneficial_owners = []
        for data in l:
            beneficial_owners.append(BeneficialOwner(data.get("fullName"), data.get("dateOfBirth"), data.get("address"),
                data.get("phone"), data.get("email"), data.get("status"), data.get("ssn"),
                data.get("passport"), data.get("nationality"), data.get("percentage")))
        return beneficial_owners


class AuthorizedUser(object):
    def __init__(self, full_name: FullName, email: str, phone: Phone):
        self.full_name = full_name
        self.email = email
        self.phone = phone

    @staticmethod
    def from_json_api(l: list):
        authorized_users = []
        for data in l:
            authorized_users.append(AuthorizedUser(data.get("fullName"), data.get("phone"), data.get("email")))
        return authorized_users

class WireCounterparty(object):
    def __init__(self, routing_number: str, account_number: str, name: str, address: Address):
        self.routing_number = routing_number
        self.account_number = account_number
        self.name = name
        self.address = address

    @staticmethod
    def from_json_api(data: dict):
        return WireCounterparty(data["routingNumber"], data["accountNumber"], data["name"],
                                Address.from_json_api(data["address"]))

class Counterparty(object):
    def __init__(self, routing_number: str, account_number: str, account_type: str, name: str):
        self.routing_number = routing_number
        self.account_number = account_number
        self.account_type = account_type
        self.name = name

    @staticmethod
    def from_json_api(data: dict):
        return Counterparty(data["routingNumber"], data["accountNumber"], data["accountType"], data["name"])

class Coordinates(object):
    def __init__(self, longitude: int, latitude: int):
        self.longitude = longitude
        self.latitude = latitude

    @staticmethod
    def from_json_api(data: dict):
        return Coordinates(data["longitude"], data["latitude"])


class Merchant(object):
    def __init__(self, name: str, type: int, category: str, location: Optional[str]):
        self.name = name
        self.type = type
        self.category = category
        self.location = location

    @staticmethod
    def from_json_api(data: dict):
        return Merchant(data["name"], data["type"], data["category"], data.get("location"))