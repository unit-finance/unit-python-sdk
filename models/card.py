import json
from datetime import datetime, date
from typing import Literal, Optional
from utils import date_utils
from models import *

CardStatus = Literal["Inactive", "Active", "Stolen", "Lost", "Frozen", "ClosedByCustomer", "SuspectedFraud"]


class IndividualDebitCardDTO(object):
    def __init__(self, id: str, created_at: datetime, last_4_digits: str, expiration_date: str, status: CardStatus,
                 shipping_address: Optional[Address], design: Optional[str], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = "individualDebitCard"
        self.created_at = created_at
        self.last_4_digits = last_4_digits
        self.expiration_date = expiration_date
        self.status = status
        self.shipping_address = shipping_address
        self.design = design
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return IndividualDebitCardDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["last4Digits"], attributes["expirationDate"],
            attributes["status"], attributes.get("shippingAddress"), attributes.get("design"), relationships
        )


class BusinessDebitCardDTO(object):
    def __init__(self, id: str, created_at: datetime, last_4_digits: str, expiration_date: str, ssn: str,
                 full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str, status: CardStatus,
                 passport: Optional[str], nationality: Optional[str], shipping_address: Optional[Address], design: Optional[str],
                 relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = "businessDebitCard"
        self.created_at = created_at
        self.last_4_digits = last_4_digits
        self.expiration_date = expiration_date
        self.ssn = ssn
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone = phone
        self.email = email
        self.status = status
        self.passport = passport
        self.nationality = nationality
        self.shipping_address = shipping_address
        self.design = design
        self.relationships = relationships

    def from_json_api(_id, _type, attributes, relationships):
        return BusinessDebitCardDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["last4Digits"], attributes["expirationDate"],
            attributes["ssn"], attributes["fullName"], attributes["dateOfBirth"], attributes["address"], attributes["phone"],
            attributes["email"], attributes["status"],  attributes.get("passport"), attributes.get("nationality"),
            attributes.get("shippingAddress"), attributes.get("design"), relationships
        )


class IndividualVirtualDebitCardDTO(object):
    def __init__(self, id: str, created_at: datetime, last_4_digits: str, expiration_date: str, status: CardStatus,
                 relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = "individualVirtualDebitCard"
        self.created_at = created_at
        self.last_4_digits = last_4_digits
        self.expiration_date = expiration_date
        self.status = status
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return IndividualDebitCardDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["last4Digits"], attributes["expirationDate"],
            attributes["status"], relationships
        )


class BusinessVirtualDebitCardDTO(object):
    def __init__(self, id: str, created_at: datetime, last_4_digits: str, expiration_date: str, ssn: str,
                 full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str, status: CardStatus,
                 passport: Optional[str], nationality: Optional[str], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = "businessVirtualDebitCard"
        self.created_at = created_at
        self.last_4_digits = last_4_digits
        self.expiration_date = expiration_date
        self.ssn = ssn
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone = phone
        self.email = email
        self.status = status
        self.passport = passport
        self.nationality = nationality
        self.relationships = relationships

    def from_json_api(_id, _type, attributes, relationships):
        return BusinessVirtualDebitCardDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["last4Digits"], attributes["expirationDate"],
            attributes["ssn"], attributes["fullName"], attributes["dateOfBirth"], attributes["address"], attributes["phone"],
            attributes["email"], attributes["status"],  attributes.get("passport"), attributes.get("nationality"), relationships
        )

Card = Union[IndividualDebitCardDTO, BusinessDebitCardDTO, IndividualVirtualDebitCardDTO, BusinessVirtualDebitCardDTO]
