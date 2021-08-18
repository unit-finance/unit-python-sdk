import json
from datetime import datetime, date
from typing import Literal, Optional
from utils import date_utils

from models import *

ApplicationStatus = Literal["Approved", "Denied", "Pending", "PendingReview"]
EntityType = Literal["Corporation", "LLC", "Partnership"]


class IndividualApplicationDTO(object):
    def __init__(self, id: str, created_at: datetime, full_name: FullName, address: Address, date_of_birth: date,
                 email: str, phone: Phone, status: ApplicationStatus, ssn: Optional[str], message: Optional[str],
                 ip: Optional[str], ein: Optional[str], dba: Optional[str],
                 sole_proprietorship: Optional[bool], tags: Optional[dict[str, str]],
                 relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = "individualApplication"
        self.created_at = created_at
        self.full_name = full_name
        self.address = address
        self.date_of_birth = date_of_birth
        self.email = email
        self.phone = phone
        self.status = status
        self.ssn = ssn
        self.message = message
        self.ip = ip
        self.ein = ein
        self.dba = dba
        self.sole_proprietorship = sole_proprietorship
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return IndividualApplicationDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]),
            FullName.from_json_api(attributes["fullName"]), Address.from_json_api(attributes["address"]),
            date_utils.to_date(attributes["dateOfBirth"]),
            attributes["email"], Phone.from_json_api(attributes["phone"]), attributes["status"],
            attributes.get("ssn"), attributes.get("message"), attributes.get("ip"),
            attributes.get("ein"), attributes.get("dba"), attributes.get("soleProprietorship"),
            attributes.get("tags"), relationships
        )


class BusinessApplicationDTO(object):
    def __init__(self, id: str, created_at: datetime, name: str, address: Address, phone: Phone,
                 status: ApplicationStatus, state_of_incorporation: str, entity_type: EntityType,
                 contact: BusinessContact, officer: Officer, beneficial_owners: [BeneficialOwner], ssn: Optional[str],
                 message: Optional[str], ip: Optional[str], ein: Optional[str], dba: Optional[str],
                 tags: Optional[dict[str, str]], relationships: Optional[dict[str, Relationship]]):
        self.id = id
        self.type = "businessApplication"
        self.created_at = created_at
        self.name = name
        self.address = address
        self.phone = phone
        self.status = status
        self.state_of_incorporation = state_of_incorporation
        self.ssn = ssn
        self.message = message
        self.ip = ip
        self.ein = ein
        self.entity_type = entity_type
        self.dba = dba
        self.contact = contact
        self.officer = officer
        self.beneficial_owners = beneficial_owners
        self.tags = tags
        self.relationships = relationships


    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessApplicationDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]),attributes.get("name"),
            Address.from_json_api(attributes["address"]), Phone.from_json_api(attributes["phone"]), attributes["status"],
            attributes.get("stateOfIncorporation"), attributes.get("entityType"),
            BusinessContact.from_json_api(attributes["contact"]), Officer.from_json_api(attributes["officer"]),
            BeneficialOwner.from_json_api(attributes["beneficialOwners"]),  attributes.get("ssn"), attributes.get("message"),
            attributes.get("ip"), attributes.get("ein"), attributes.get("dba"), attributes.get("tags"), relationships
        )


class CreateIndividualApplicationRequest(UnitRequest):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, email: str, phone: Phone,
                 ip: str = None, ein: str = None, dba: str = None, sole_proprietorship: bool = None, ssn=None):
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.email = email
        self.phone = phone
        self.ip = ip
        self.ein = ein
        self.dba = dba
        self.sole_proprietorship = sole_proprietorship
        self.ssn = ssn

    def to_json_api(self) -> dict:
        payload = {
            "data": {
                "type": "individualApplication",
                "attributes": {
                    "ssn": self.ssn,
                    "fullName": self.full_name,
                    "dateOfBirth": date_utils.to_date_str(self.date_of_birth),
                    "address": self.address,
                    "email": self.email,
                    "phone": self.phone,
                }
            }
        }

        if self.ip:
            payload["data"]["attributes"]["ip"] = self.ip

        if self.ein:
            payload["data"]["attributes"]["ein"] = self.ein

        if self.dba:
            payload["data"]["attributes"]["dba"] = self.dba

        if self.sole_proprietorship:
            payload["data"]["attributes"]["soleProprietorship"] = self.sole_proprietorship

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class CreateBusinessApplicationRequest(UnitRequest):
    def __init__(self, name: str, address: Address, phone: Phone, state_of_incorporation: str, ein: str,
                 contact: BusinessContact, officer: Officer, beneficial_owners: [BeneficialOwner],
                 entity_type: EntityType, dba: str = None, ip: str = None, website: str = None):
        self.name = name
        self.address = address
        self.phone = phone
        self.state_of_incorporation = state_of_incorporation
        self.ein = ein
        self.contact = contact
        self.officer = officer
        self.beneficial_owners = beneficial_owners
        self.entity_type = entity_type
        self.dba = dba
        self.ip = ip
        self.website = website

    def to_json_api(self) -> dict:
        payload = {
            "data": {
                "type": "businessApplication",
                "attributes": {
                    "name": self.name,
                    "address": self.address,
                    "phone": self.phone,
                    "stateOfIncorporation": self.state_of_incorporation,
                    "ein": self.ein,
                    "contact": self.contact,
                    "officer": self.officer,
                    "beneficialOwners": self.beneficial_owners,
                    "entityType": self.entity_type
                }
            }
        }

        if self.dba:
            payload["data"]["attributes"]["dba"] = self.dba

        if self.ip:
            payload["data"]["attributes"]["ip"] = self.ip

        if self.website:
            payload["data"]["attributes"]["website"] = self.website

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


ApplicationDTO = Union[IndividualApplicationDTO, BusinessApplicationDTO]
