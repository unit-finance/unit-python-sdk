import os
import unittest
from unit import Unit
from unit.models.applicationForm import CreateApplicationFormRequest


class ApplicationFormE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)
    card_types = ["individualDebitCard", "businessDebitCard", "individualVirtualDebitCard", "businessVirtualDebitCard"]

    def create_create_application_form(self):
        request = CreateApplicationFormRequest(tags={"userId": "106a75e9-de77-4e25-9561-faffe59d7814"},
                                               allowed_application_types=["Individual"])
        return self.client.applicationForms.create(request)

    def test_create_application_form(self):
        response = self.create_create_application_form()
        self.assertTrue(response.data.type == "applicationForm")

    def test_get_application_form(self):
        application_form_id = self.create_create_application_form().data.id
        response = self.client.applicationForms.get(application_form_id)
        self.assertTrue(response.data.type == "applicationForm")

    def test_list_application_form(self):
        response = self.client.applicationForms.list()
        for app in response.data:
            self.assertTrue(app.type == "applicationForm")


if __name__ == '__main__':
    unittest.main()

