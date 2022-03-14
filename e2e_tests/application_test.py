import os
import unittest
from datetime import timedelta
from unit import Unit
from unit.models.application import *


class ApplicationE2eTests(unittest.TestCase):
    def create_individual_application(self):
        token = os.environ.get("token")

        device_fingerprint = DeviceFingerprint.from_json_api({
            "provider": "iovation",
            "value": "0400bpNfiPCR/AUNf94lis1ztpaNnzv+lNq30Hfp5ie720z/CiIC8ERuu3YpPgQiEVyiFhADfeGQZO28FbUrrO5N6T/KhUgGeNqKfeXqFvOptJMkxZw+Y9UPy+f0N3IyJgvEw8TWskb/j+GHTKUkZ8zWbl1IO8WxD1Kht8TqEibpebBOV3otSIldf1zxXVkhYr77KTMIYGWCBwYibAjilOCqFmMCwwZ2fQOGTEVdGJlxBwCc8acbcKqAuWf7gouzBPJaEMCy0s3hRLlX3uHnT/mMq7bvVoECdF71JNfXVRZenju64Ouq7Dncq6Dl1FsZY8jwYa/hFBBVErqVT31SgfbGSd1k0e/YM3Dtt6SI2G2F/ThwR+CXcWdbH3hXufQCF6M4Dpgq27WF46865RaUe/IZRl+rdsbATajAyMeRup82fY15RZwU9zPDpHaSwVqaWdUNw+E1ob+/FRCJ3uese38lURah37+pYGav2UwkTNot/DgwZ8YN8wmMva0q3Wpvwm165E+YRS8maek+P03Li8QHdLmZnC9N+MV7Pw1IrivGG+SXG7Fg5ZExEZyxlgiYsdKgDX8icOWPZcy4Xo6JR+o8uNh2BeaMmRyXBtJlds64QOcTfWwKrqPu/ordrByteUo8YUcRNcJsz+1j3aE1Kav6TbwSyw9pfmqz7J9hKqYUy8nou5GL7lS1H1jks3/PBPSgsZBfgyIR+XyE6hsi11FUlhkwfCqvl92YChvQ5GutOWzcgAlm5C655YuD71qCKcmZqa+c5UMfdLNXqLz+1vlqUAr9dE2jcfl0wgroQBfpyuI++K9SiDi/XDMkV0rONHETVTw2C4oQ2p6vWc20/w4QKST/riUqiozfAOitx40UDzaLaxNWMM2S8Us77dixCJm6Q57yZdeR90iPaqS7dmS/Ocl5HQBNDFBWeVaYJEF00M2y5rEDAARtF2ONlKQFMFWIfGA9WPh4380ZhZzwCZq88ApXlgSYdPkGU/BN8NSHlLSYTdGrUGXc9xYjcWtBi6X2zTt76b5csU1EK0+sD0E3ZqRPV+2/f5evS5h4cLbW2EYqYNCw25rZJOp9wXDoTKUQQlPiadkVLXwMpOFU/WEDIOxhmgTkbsvKHRH29E2Pl68vN0XpeFtRx/cjdbgHxEkRmgkRq1Qs48sbX9QC8nOTD0ntb6FcJyEOEOVzmJtDqimkzDq+SXR1/7oj0f6YtJc05sdrzcINkHr+mxLg5xX0cvFOwbohKb3xCPSKMsCJXe4s152+pJeKAyZP60EH4fIPPSI7lrfThjSC+ZC/uhKlHiPzk7Wcbftiipgbt5tQ5DBgOa5eE3shSuCUuzjuYSvn4NHYYO+c6svSooIPnW146zqeKNiPJcgsVSaircwUTU6esiGRHxaLYuc0891K2c1Zd7VesgONPiXcBur/JCDJyOWRcJ2nAB+S9dSneRnhcIA="
        })

        request = CreateIndividualApplicationRequest(
            FullName("Jhon", "Doe"), date.today() - timedelta(days=20*365),
            Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500", "US"), "jone.doe1@unit-finance.com",
            Phone("1", "2025550108"),
            ssn="000000003",
            device_fingerprints=[device_fingerprint]
        )

        client = Unit("https://api.s.unit.sh", token)
        return client.applications.create(request)

    def test_create_individual_application(self):
        app = self.create_individual_application()
        self.assertTrue(app.data.type == "individualApplication")

    def test_create_business_application(self):
        token = os.environ.get("token")
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

        client = Unit("https://api.s.unit.sh", token)
        response = client.applications.create(request)
        self.assertTrue(response.data.type == "businessApplication")

    def test_get_applications(self):
        token = os.environ.get("token")
        client = Unit("https://api.s.unit.sh", token)
        response = client.applications.get("72996")
        self.assertTrue(response.data.type == "businessApplication" or response.data.type == "individualApplication")

    def test_list_applications(self):
        token = os.environ.get("token")
        client = Unit("https://api.s.unit.sh", token)
        response = client.applications.list()
        for app in response.data:
            self.assertTrue(app.type == "businessApplication" or app.type == "individualApplication")

    def test_upload_application_document(self):
        token = os.environ.get("token")
        client = Unit("https://api.s.unit.sh", token)
        app = self.create_individual_application()
        doc_id = app.included[0].id
        with open("../sample.pdf", 'rb') as file:
            request = UploadDocumentRequest(app.data.id, doc_id, file.read(), "pdf")
        response = client.applications.upload(request)
        self.assertTrue(response.data.type == "document")

    def test_upload_application_back_document(self):
        token = os.environ.get("token")
        client = Unit("https://api.s.unit.sh", token)
        app = self.create_individual_application()
        doc_id = app.included[0].id
        with open("../sample.pdf", 'rb') as file:
            request = UploadDocumentRequest(app.data.id, doc_id, file.read(), "pdf", True)
        response = client.applications.upload(request)
        self.assertTrue(response.data.type == "document")



if __name__ == '__main__':
    unittest.main()

