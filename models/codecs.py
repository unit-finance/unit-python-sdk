import json
from models import *
from datetime import datetime, date
from utils import date_utils
from models.application import IndividualApplicationDTO, BusinessApplicationDTO, ApplicationDocumentDTO
from models.customer import IndividualCustomerDTO, BusinessCustomerDTO

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
    }


def split_json_api_single_response(payload: dict):
    _id, _type, attributes = payload["id"], payload["type"], payload["attributes"]
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
            officer = {"fullName": obj.full_name, "dateOfBirth": date_utils.to_date_str(obj.date_of_birth), "address": obj.address,
                    "phone": obj.phone, "email": obj.email}
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
            beneficial_owner = {"fullName": obj.full_name, "dateOfBirth": date_utils.to_date_str(obj.date_of_birth), "address": obj.address,
                                "phone": obj.phone, "email": obj.email}
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
        return json.JSONEncoder.default(self, obj)
