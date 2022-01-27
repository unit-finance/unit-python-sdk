import os
import unittest
from datetime import timedelta
from unit import Unit
from unit.models.application import *


class ApplicationE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def create_individual_application(self):
        request = CreateIndividualApplicationRequest(
            FullName("Jhon", "Doe"), date.today() - timedelta(days=20*365),
            Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500", "US"), "jone.doe1@unit-finance.com",
            Phone("1", "2025550108"),
            ssn="000000003"
        )

        return self.client.applications.create(request)

    def create_business_application(self):
        request = CreateBusinessApplicationRequest(
            name="Acme Inc.",
            address=Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500", "US"),
            phone=Phone("1", "9294723497"), state_of_incorporation="CA", entity_type="Corporation", ein="123456789",
            officer=Officer(full_name=FullName("Jone", "Doe"), date_of_birth=date.today() - timedelta(days=20 * 365),
                               address=Address("950 Allerton Street", "Redwood City", "CA", "94063", "US"),
                               phone=Phone("1", "2025550108"), email="jone.doe@unit-finance.com", ssn="000000005"),
            contact=BusinessContact(full_name=FullName("Jone", "Doe"), email="jone.doe@unit-finance.com", phone=Phone("1", "2025550108")),
            beneficial_owners=[
                BeneficialOwner(
                    FullName("James", "Smith"), date.today() - timedelta(days=20*365),
                    Address("650 Allerton Street","Redwood City","CA","94063","US"),
                    Phone("1","2025550127"),"james@unit-finance.com",ssn="574567625"),
                  BeneficialOwner(FullName("Richard","Hendricks"), date.today() - timedelta(days=20 * 365),
                  Address("470 Allerton Street", "Redwood City", "CA", "94063", "US"),
                  Phone("1", "2025550158"), "richard@unit-finance.com", ssn="574572795")
            ]
        )

        return self.client.applications.create(request)

    def test_create_individual_application(self):
        app = self.create_individual_application()
        self.assertTrue(app.data.type == "individualApplication")

    def test_create_business_application(self):
        app = self.create_business_application()
        self.assertTrue(app.data.type == "businessApplication")

    def test_get_applications(self):
        response = self.client.applications.get("72996")
        self.assertTrue(response.data.type == "businessApplication" or response.data.type == "individualApplication")

    def test_list_applications(self):
        response = self.client.applications.list()
        for app in response.data:
            self.assertTrue(app.type == "businessApplication" or app.type == "individualApplication")

    def test_upload_application_document(self):
        app = self.create_individual_application()
        doc_id = app.included[0].id
        with open("../sample.pdf", 'rb') as file:
            request = UploadDocumentRequest(app.data.id, doc_id, file.read(), "pdf")
        response = self.client.applications.upload(request)
        self.assertTrue(response.data.type == "document")

    def test_upload_application_back_document(self):
        app = self.create_individual_application()
        doc_id = app.included[0].id
        with open("../sample.pdf", 'rb') as file:
            request = UploadDocumentRequest(app.data.id, doc_id, file.read(), "pdf", True)
        response = self.client.applications.upload(request)
        self.assertTrue(response.data.type == "document")

    def test_update_individual_application(self):
        app = self.create_individual_application()
        updated = self.client.applications.update(PatchApplicationRequest(app.data.id, tags={"patch": "test-patch"}))
        self.assertTrue(updated.data.type == "individualApplication")

    def test_update_bussiness_application(self):
        app = self.create_business_application()
        updated = self.client.applications.update(PatchApplicationRequest(app.data.id, "businessApplication",
                                                                          tags={"patch": "test-patch"}))
        self.assertTrue(updated.data.type == "businessApplication")


if __name__ == '__main__':
    unittest.main()

