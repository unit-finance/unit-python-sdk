import os

from e2e_tests.helpers.helpers import create_individual_application
from unit import Unit
from unit.models import FullName, BusinessContact, Phone, Officer, Address, BeneficialOwner
from unit.models.applicationForm import CreateApplicationFormRequest, ApplicationFormPrefill

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)
card_types = ["individualDebitCard", "businessDebitCard", "individualVirtualDebitCard", "businessVirtualDebitCard"]


def create_application_form():
    ad = ApplicationFormPrefill("Business", FullName("Peter", "Parker"), "721074426", "12345678", "US", "2001-08-10",
                           "peter@oscorp.com", "Pied Piper", "DE", "Corporation",
                           BusinessContact(FullName("Richard", "Hendricks"), "richard@piedpiper.com",
                                           Phone("1", "5555555555")),
                           Officer(FullName("Richard", "Hendricks"), "2001-08-10",
                                   Address("5230 Newell Rd", "Palo Alto",  "CA", "94303", "US"),
                                   Phone("1", "5555555555"), "richard@piedpiper.com", title="COO", ssn="721074426"),
                           [BeneficialOwner(FullName("Richard", "Hendricks"), "2001-08-10",
                                            Address("5230 Newell Rd", "Palo Alto",  "CA", "94303", "US"),
                                            Phone("1", "5555555555"), "richard@piedpiper.com", ssn="123456789",
                                            percentage=75)], "https://www.piedpiper.com", "Piedpiper Inc", "123456789",
                           Address("5230 Newell Rd", "Palo Alto",  "CA", "94303", "US"), Phone("1", "5555555555"),
                           "Doctor", "Between10kAnd25k", "EmploymentOrPayrollIncome", "TechnologyMediaOrTelecom",
                           "Between500kAnd1m", "Between50And100", "Predictable", "2014", ["US", "CA"], "PPI", False)

    request = CreateApplicationFormRequest(tags={"userId": "106a75e9-de77-4e25-9561-faffe59d7814"},
                                           allowed_application_types=["Individual"],
                                           applicant_details=ad)

    return client.applicationForms.create(request)


def create_application_form_with_prefill():
    prefill = ApplicationFormPrefill(email="test@castlepay.co")

    request = CreateApplicationFormRequest(tags={"userId": "106a75e9-de77-4e25-9561-faffe59d7814"},
                                           applicant_details=prefill)

    return client.applicationForms.create(request)

def test_create_application_form():
    response = create_application_form()
    assert response.data.type == "applicationForm"

def test_create_application_form_with_prefill():
    response = create_application_form_with_prefill()
    assert response.data.type == "applicationForm"

def test_get_application_form():
    application_form_id = create_application_form().data.id
    response = client.applicationForms.get(application_form_id, "application")
    assert response.data.type == "applicationForm"

def test_list_application_form():
    response = client.applicationForms.list()
    for app in response.data:
        assert app.type == "applicationForm"


def test_create_application_form_for_application():
    application = create_individual_application(client).data
    request = CreateApplicationFormRequest(relationships={"application": {"data": {"type": "application",
                                                                                   "id": application.id}}})

    response = client.applicationForms.create(request)

    assert response.data.type == "applicationForm"

