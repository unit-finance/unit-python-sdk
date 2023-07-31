import os

from e2e_tests.helpers.helpers import create_individual_application
from unit import Unit
from unit.models.applicationForm import CreateApplicationFormRequest, ApplicationFormPrefill

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)
card_types = ["individualDebitCard", "businessDebitCard", "individualVirtualDebitCard", "businessVirtualDebitCard"]

def create_application_form():
    request = CreateApplicationFormRequest(tags={"userId": "106a75e9-de77-4e25-9561-faffe59d7814"},
                                           allowed_application_types=["Individual"],
                                           application_details={"jwtSubject": "test4"})

    return client.applicationForms.create(request)


def create_application_form_with_prefill():
    prefill = ApplicationFormPrefill(email="test@castlepay.co")

    request = CreateApplicationFormRequest(tags={"userId": "106a75e9-de77-4e25-9561-faffe59d7814"},
                                           application_details=prefill)

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

