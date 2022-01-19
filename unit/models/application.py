from unit.utils import date_utils
from unit.models import *
from typing import IO

ApplicationStatus = Literal["Approved", "Denied", "Pending", "PendingReview"]

DocumentType = Literal["IdDocument", "Passport", "AddressVerification", "CertificateOfIncorporation",
                       "EmployerIdentificationNumberConfirmation"]
ReasonCode = Literal["PoorQuality", "NameMismatch", "SSNMismatch", "AddressMismatch", "DOBMismatch", "ExpiredId",
                     "EINMismatch", "StateMismatch", "Other"]

class IndividualApplicationDTO(object):
    def __init__(self, id: str, created_at: datetime, full_name: FullName, address: Address, date_of_birth: date,
                 email: str, phone: Phone, status: ApplicationStatus, ssn: Optional[str], message: Optional[str],
                 ip: Optional[str], ein: Optional[str], dba: Optional[str],
                 sole_proprietorship: Optional[bool], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "individualApplication"
        self.attributes = {"createdAt": created_at, "fullName": full_name, "address": address,
                           "dateOfBirth": date_of_birth, "email": email, "phone": phone, "status": status, "ssn": ssn,
                           "message": message, "ip": ip, "ein": ein, "dba": dba,
                           "soleProprietorship": sole_proprietorship, "tags": tags}
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
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "businessApplication"
        self.attributes = {"createdAt": created_at, "name": name, "address": address, "phone": phone,
                           "status": status, "ssn": ssn, "stateOfIncorporation": state_of_incorporation, "ssn": ssn,
                           "message": message, "ip": ip, "ein": ein, "entityType": entity_type, "dba": dba,
                           "contact": contact, "officer": officer, "beneficialOwners":beneficial_owners, "tags": tags}
        self.relationships = relationships


    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BusinessApplicationDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes.get("name"),
            Address.from_json_api(attributes["address"]), Phone.from_json_api(attributes["phone"]),
            attributes["status"], attributes.get("stateOfIncorporation"), attributes.get("entityType"),
            BusinessContact.from_json_api(attributes["contact"]), Officer.from_json_api(attributes["officer"]),
            BeneficialOwner.from_json_api(attributes["beneficialOwners"]),  attributes.get("ssn"),
            attributes.get("message"), attributes.get("ip"), attributes.get("ein"), attributes.get("dba"),
            attributes.get("tags"), relationships
        )

ApplicationDTO = Union[IndividualApplicationDTO, BusinessApplicationDTO]

class CreateIndividualApplicationRequest(UnitRequest):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, email: str, phone: Phone,
                 ip: str = None, ein: str = None, dba: str = None, sole_proprietorship: bool = None, ssn = None):
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

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "individualApplication",
                "attributes": {
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

        if self.ssn:
            payload["data"]["attributes"]["ssn"] = self.ssn

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

    def to_json_api(self) -> Dict:
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


class ApplicationDocumentDTO(object):
    def __init__(self, id: str, status: ApplicationStatus, document_type: DocumentType, description: str, name: str,
                 address: Optional[Address], date_of_birth: Optional[date], passport: Optional[str], ein: Optional[str],
                 reason_code: Optional[ReasonCode], reason: Optional[str]):
        self.id = id
        self.type = "document"
        self.attributes = {"status": status, "documentType": document_type, "description": description, "name": name,
                           "address": address, "dateOfBirth": date_of_birth, "passport": passport, "ein": ein,
                           "reasonCode": reason_code, "reason": reason}

    @staticmethod
    def from_json_api(_id, _type, attributes):
        address = Address.from_json_api(attributes.get("address")) if attributes.get("address") else None
        return ApplicationDocumentDTO(
            _id, attributes["status"], attributes["documentType"], attributes["description"], attributes["name"],
            address, attributes.get("dateOfBirth"), attributes.get("passport"),
            attributes.get("ein"), attributes.get("reasonCode"), attributes.get("reason")
        )

FileType = Literal["jpeg", "png", "pdf"]


class UploadDocumentRequest(object):
    def __init__(self, application_id: str, document_id: str, file: IO, file_type: FileType,
                 is_back_side: Optional[bool] = False):
        self.application_id = application_id
        self.document_id = document_id
        self.file = file
        self.file_type = file_type
        self.is_back_side = is_back_side


class ListApplicationParams(UnitParams):
    def __init__(self, offset: int = 0, limit: int = 100, email: Optional[str] = None,
                 tags: Optional[object] = None, query: Optional[str] = None,
                 sort: Optional[Literal["createdAt", "-createdAt"]] = None):
        self.offset = offset
        self.limit = limit
        self.email = email
        self.query = query
        self.sort = sort
        self.tags = tags
        
    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.email:
            parameters["filter[email]"] = self.email
        if self.query:
            parameters["filter[query]"] = self.query
        if self.tags:
            parameters["filter[tags]"] = self.tags
        if self.sort:
            parameters["sort"] = self.sort
        return parameters
    