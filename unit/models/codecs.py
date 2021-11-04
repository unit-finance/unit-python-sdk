import json
from unit.models import *
from datetime import datetime, date
from unit.utils import date_utils
from unit.models.applicationForm import ApplicationFormDTO
from unit.models.application import IndividualApplicationDTO, BusinessApplicationDTO, ApplicationDocumentDTO
from unit.models.account import DepositAccountDTO, AccountLimitsDTO
from unit.models.customer import IndividualCustomerDTO, BusinessCustomerDTO
from unit.models.card import IndividualDebitCardDTO, BusinessDebitCardDTO, IndividualVirtualDebitCardDTO, BusinessVirtualDebitCardDTO
from unit.models.transaction import *
from unit.models.payment import AchPaymentDTO, BookPaymentDTO, WirePaymentDTO
from unit.models.customerToken import CustomerTokenDTO, CustomerVerificationTokenDTO

mappings = {
        "individualApplication": lambda _id, _type, attributes, relationships:
        IndividualApplicationDTO.from_json_api(_id, _type, attributes, relationships),

        "businessApplication": lambda _id, _type, attributes, relationships:
        BusinessApplicationDTO.from_json_api(_id, _type, attributes, relationships),

        "document": lambda _id, _type, attributes, relationships:
        ApplicationDocumentDTO.from_json_api(_id, _type, attributes),

        "individualCustomer": lambda _id, _type, attributes, relationships:
        IndividualCustomerDTO.from_json_api(_id, _type, attributes, relationships),

        "businessCustomer": lambda _id, _type, attributes, relationships:
        BusinessCustomerDTO.from_json_api(_id, _type, attributes, relationships),

        "depositAccount": lambda _id, _type, attributes, relationships:
        DepositAccountDTO.from_json_api(_id, _type, attributes, relationships),

        "limits": lambda _id, _type, attributes, relationships:
        AccountLimitsDTO.from_json_api(_type, attributes),

        "individualDebitCard": lambda _id, _type, attributes, relationships:
        IndividualDebitCardDTO.from_json_api(_id, _type, attributes, relationships),

        "businessDebitCard": lambda _id, _type, attributes, relationships:
        BusinessDebitCardDTO.from_json_api(_id, _type, attributes, relationships),

        "individualVirtualDebitCard": lambda _id, _type, attributes, relationships:
        IndividualVirtualDebitCardDTO.from_json_api(_id, _type, attributes, relationships),

        "businessVirtualDebitCard": lambda _id, _type, attributes, relationships:
        BusinessVirtualDebitCardDTO.from_json_api(_id, _type, attributes, relationships),

        "originatedAchTransaction": lambda _id, _type, attributes, relationships:
        OriginatedAchTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "receivedAchTransaction": lambda _id, _type, attributes, relationships:
        ReceivedAchTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "returnedAchTransaction": lambda _id, _type, attributes, relationships:
        ReturnedAchTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "returnedReceivedAchTransaction": lambda _id, _type, attributes, relationships:
        ReturnedReceivedAchTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "dishonoredAchTransaction": lambda _id, _type, attributes, relationships:
        DishonoredAchTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "bookTransaction": lambda _id, _type, attributes, relationships:
        BookTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "purchaseTransaction": lambda _id, _type, attributes, relationships:
        PurchaseTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "atmTransaction": lambda _id, _type, attributes, relationships:
        AtmTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "feeTransaction": lambda _id, _type, attributes, relationships:
        FeeTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "cardTransaction": lambda _id, _type, attributes, relationships:
        CardTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "wireTransaction": lambda _id, _type, attributes, relationships:
        WireTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "releaseTransaction": lambda _id, _type, attributes, relationships:
        ReleaseTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "adjustmentTransaction": lambda _id, _type, attributes, relationships:
        AdjustmentTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "interestTransaction": lambda _id, _type, attributes, relationships:
        InterestTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "disputeTransaction": lambda _id, _type, attributes, relationships:
        DisputeTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "checkDepositTransaction": lambda _id, _type, attributes, relationships:
        CheckDepositTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "returnedCheckDepositTransaction": lambda _id, _type, attributes, relationships:
        ReturnedCheckDepositTransactionDTO.from_json_api(_id, _type, attributes, relationships),

        "achPayment": lambda _id, _type, attributes, relationships:
        AchPaymentDTO.from_json_api(_id, _type, attributes, relationships),

        "bookPayment": lambda _id, _type, attributes, relationships:
        BookPaymentDTO.from_json_api(_id, _type, attributes, relationships),

        "wirePayment": lambda _id, _type, attributes, relationships:
        WirePaymentDTO.from_json_api(_id, _type, attributes, relationships),

        "customerBearerToken": lambda _id, _type, attributes, relationships:
        CustomerTokenDTO.from_json_api(_id, _type, attributes, relationships),

        "customerTokenVerification": lambda _id, _type, attributes, relationships:
        CustomerVerificationTokenDTO.from_json_api(_id, _type, attributes, relationships),

        "applicationForm": lambda _id, _type, attributes, relationships:
        ApplicationFormDTO.from_json_api(_id, _type, attributes, relationships),

    }


def split_json_api_single_response(payload: dict):
    _id, _type, attributes = payload.get("id"), payload["type"], payload["attributes"]
    relationships = None

    if payload.get("relationships"):
        relationships = dict()
        for k, v in payload.get("relationships").items():
            if isinstance(v["data"], list):
                # todo: alex handle cases when relationships are in a form of array (e.g. jointAccount or documents)
                continue
            else:
                relationships[k] = Relationship(v["data"]["type"], v["data"]["id"])

    return _id, _type, attributes, relationships


def split_json_api_array_response(payload):
    if not isinstance(payload, list):
        raise Exception("split_json_api_array_response - couldn't parse response.")

    dtos = []
    for single_obj in payload:
        dtos.append(split_json_api_single_response(single_obj))

    return dtos


class DtoDecoder(object):
    @staticmethod
    def decode(payload):
        if payload is None:
            return None
        # if response contains a list of dtos
        if isinstance(payload, list):
            dtos = split_json_api_array_response(payload)
            response = []
            for _id, _type, attributes, relationships in dtos:
                response.append(mappings[_type](_id, _type, attributes, relationships))

            return response
        else:
            _id, _type, attributes, relationships = split_json_api_single_response(payload)
            return mappings[_type](_id, _type, attributes, relationships)


class UnitEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FullName):
            return {"first": obj.first, "last": obj.last}
        if isinstance(obj, Phone):
            return {"countryCode": obj.country_code, "number": obj.number}
        if isinstance(obj, Address):
            addr = {
                "street": obj.street,
                "city": obj.city,
                "state": obj.state,
                "postalCode": obj.postal_code,
                "country": obj.country
            }

            if obj.street2 is not None:
                addr["street2"] = obj.street2
            return addr
        if isinstance(obj, BusinessContact):
            return {"fullName": obj.full_name, "email": obj.email, "phone": obj.phone}
        if isinstance(obj, Officer):
            officer = {"fullName": obj.full_name, "dateOfBirth": date_utils.to_date_str(obj.date_of_birth),
                       "address": obj.address, "phone": obj.phone, "email": obj.email}
            if obj.status is not None:
                officer["status"] = obj.status
            if obj.title is not None:
                officer["title"] = obj.title
            if obj.ssn is not None:
                officer["ssn"] = obj.ssn
            if obj.passport is not None:
                officer["passport"] = obj.passport
            if obj.nationality is not None:
                officer["nationality"] = obj.nationality
            return officer
        if isinstance(obj, BeneficialOwner):
            beneficial_owner = {"fullName": obj.full_name, "dateOfBirth": date_utils.to_date_str(obj.date_of_birth),
                                "address": obj.address, "phone": obj.phone, "email": obj.email}
            if obj.status is not None:
                beneficial_owner["status"] = obj.status
            if obj.ssn is not None:
                beneficial_owner["ssn"] = obj.ssn
            if obj.passport is not None:
                beneficial_owner["passport"] = obj.passport
            if obj.nationality is not None:
                beneficial_owner["nationality"] = obj.nationality
            if obj.percentage is not None:
                beneficial_owner["percentage"] = obj.percentage
            return beneficial_owner
        if isinstance(obj, RelationshipArray):
            return {"data": list(map(lambda r: r.to_dict(), obj.relationships))}
        if isinstance(obj, Relationship):
            return {"data": obj.to_dict()}
        if isinstance(obj, Counterparty):
            return {"routingNumber": obj.routingNumber, "accountNumber": obj.accountNumber,
                    "accountType": obj.accountType, "name": obj.name}
        if isinstance(obj, Coordinates):
            return {"longitude": obj.longitude, "latitude": obj.latitude}
        return json.JSONEncoder.default(self, obj)
