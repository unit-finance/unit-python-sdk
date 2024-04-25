import json
from typing import Optional
from unit.models import *
from unit.utils import date_utils


class BenificialOwnerDTO(object):
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
    def from_json_api(attributes):
        return BenificialOwnerDTO(attributes.get("fullName"), attributes.get("dateOfBirth"), attributes.get("address"),
                                                 attributes.get("phone"), attributes.get("email"), attributes.get("status"), attributes.get("ssn"),
                                                 attributes.get("passport"), attributes.get("nationality"), attributes.get("percentage"))