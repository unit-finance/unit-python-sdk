import json
from typing import TypeVar, Generic, Union, Optional


class Relationship(object):
    def __init__(self, _type: str, _id: str):
        self.type = _type
        self.id = _id


T = TypeVar('T')


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
    def __init__(self, title: str, status: str, detail: Optional[str] = None, details: Optional[str] = None, source: Optional[dict] = None):
        self.title = title
        self.status = status
        self.detail = detail
        self.details = details
        self.source = source


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


class FullName(object):
    def __init__(self, first: str, last: str):
        self.first = first
        self.last = last

    @staticmethod
    def from_json_api(data: dict):
        FullName(data.get("first"), data.get("last"))


# todo: Alex - use typing.Literal for multi accepted values (e.g country)
class Address(object):
    def __init__(self, street: str, city: str, state: str, postal_code: str, country: str, street2: Optional[str] = None):
        self.street = street
        self.street2 = street2
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country

    @staticmethod
    def from_json_api(data: dict):
        Address(data.get("street"), data.get("city"), data.get("state"),
                data.get("postal_code"), data.get("country"), data.get("street2", None))


class Phone(object):
    def __init__(self, country_code: str, number: str):
        self.country_code = country_code
        self.number = number

    @staticmethod
    def from_json_api(data: dict):
        Phone(data.get("country_code"), data.get("number"))
