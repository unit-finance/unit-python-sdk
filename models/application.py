import json
from datetime import datetime, date
from typing import Literal, Optional
from utils import date_utils

from models import *

ApplicationStatus = Literal["Approved", "Denied", "Pending", "PendingReview"]
DocumentType = Literal["IdDocument", "Passport", "AddressVerification", "CertificateOfIncorporation",
                       "EmployerIdentificationNumberConfirmation"]
ReasonCode = Literal["PoorQuality", "NameMismatch", "SSNMismatch", "AddressMismatch", "DOBMismatch", "ExpiredId",
                     "EINMismatch", "StateMismatch", "Other"]

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
            FullName.from_json_api(attributes), Address.from_json_api(attributes),
            date_utils.to_date(attributes["dateOfBirth"]),
            attributes["email"], Phone.from_json_api(attributes), attributes["status"],
            attributes.get("ssn"), attributes.get("message"), attributes.get("ip"),
            attributes.get("ein"), attributes.get("dba"), attributes.get("soleProprietorship"),
            attributes.get("tags"), relationships
        )


class BusinessApplicationDTO(object):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        pass


class CreateIndividualApplicationRequest(UnitRequest):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, email: str, phone: Phone, ip: str = None, ein: str = None, dba: str = None, sole_proprietorship : bool = None, ssn=None):
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
    def to_json_api(self) -> str:
        pass


class ApplicationDocumentDTO(object):
    def __init__(self, id: str, status: ApplicationStatus, documentType: DocumentType, description: str, name: str,
                 address: Optional[Address], date_of_birth: Optional[date], passport: Optional[str], ein: Optional[str],
                 reasonCode: Optional[ReasonCode], reason: Optional[str]):
        self.id = id
        self.type = "document"
        self.status = status
        self.documentType = documentType
        self.description = description
        self.address = address
        self.date_of_birth = date_of_birth
        self.passport = passport
        self.ein = ein
        self.reasonCode = reasonCode
        self.reason = reason
        self.tags = tags
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes):
        return ApplicationDocument(
            _id, attributes["status"], attributes["documentType"], attributes["description"], attributes["name"],
            attributes["address"], date_utils.to_datetime(attributes["dateOfBirth"]),attributes["passport"],
            attributes["ein"], attributes["reasonCode"], attributes["reason"]
        )


ApplicationDTO = Union[IndividualApplicationDTO, BusinessApplicationDTO]
