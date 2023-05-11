import os
from unit import Unit, Configuration
from unit.models.application import *
from e2e_tests.helpers.helpers import *
from unit.models.codecs import DtoDecoder

token = os.environ.get('TOKEN')
c = Configuration("https://api.s.unit.sh", token, 2, 150)
client = Unit(configuration=c)


ApplicationTypes = ["individualApplication", "businessApplication", "trustApplication"]


def create_individual_application(ssn: str = "000000003"):
    device_fingerprint = DeviceFingerprint.from_json_api({
        "provider": "iovation",
        "value": "0400bpNfiPCR/AUNf94lis1ztpaNnzv+lNq30Hfp5ie720z/CiIC8ERuu3YpPgQiEVyiFhADfeGQZO28FbUrrO5N6T/KhUgGeNqKfeXqFvOptJMkxZw+Y9UPy+f0N3IyJgvEw8TWskb/j+GHTKUkZ8zWbl1IO8WxD1Kht8TqEibpebBOV3otSIldf1zxXVkhYr77KTMIYGWCBwYibAjilOCqFmMCwwZ2fQOGTEVdGJlxBwCc8acbcKqAuWf7gouzBPJaEMCy0s3hRLlX3uHnT/mMq7bvVoECdF71JNfXVRZenju64Ouq7Dncq6Dl1FsZY8jwYa/hFBBVErqVT31SgfbGSd1k0e/YM3Dtt6SI2G2F/ThwR+CXcWdbH3hXufQCF6M4Dpgq27WF46865RaUe/IZRl+rdsbATajAyMeRup82fY15RZwU9zPDpHaSwVqaWdUNw+E1ob+/FRCJ3uese38lURah37+pYGav2UwkTNot/DgwZ8YN8wmMva0q3Wpvwm165E+YRS8maek+P03Li8QHdLmZnC9N+MV7Pw1IrivGG+SXG7Fg5ZExEZyxlgiYsdKgDX8icOWPZcy4Xo6JR+o8uNh2BeaMmRyXBtJlds64QOcTfWwKrqPu/ordrByteUo8YUcRNcJsz+1j3aE1Kav6TbwSyw9pfmqz7J9hKqYUy8nou5GL7lS1H1jks3/PBPSgsZBfgyIR+XyE6hsi11FUlhkwfCqvl92YChvQ5GutOWzcgAlm5C655YuD71qCKcmZqa+c5UMfdLNXqLz+1vlqUAr9dE2jcfl0wgroQBfpyuI++K9SiDi/XDMkV0rONHETVTw2C4oQ2p6vWc20/w4QKST/riUqiozfAOitx40UDzaLaxNWMM2S8Us77dixCJm6Q57yZdeR90iPaqS7dmS/Ocl5HQBNDFBWeVaYJEF00M2y5rEDAARtF2ONlKQFMFWIfGA9WPh4380ZhZzwCZq88ApXlgSYdPkGU/BN8NSHlLSYTdGrUGXc9xYjcWtBi6X2zTt76b5csU1EK0+sD0E3ZqRPV+2/f5evS5h4cLbW2EYqYNCw25rZJOp9wXDoTKUQQlPiadkVLXwMpOFU/WEDIOxhmgTkbsvKHRH29E2Pl68vN0XpeFtRx/cjdbgHxEkRmgkRq1Qs48sbX9QC8nOTD0ntb6FcJyEOEOVzmJtDqimkzDq+SXR1/7oj0f6YtJc05sdrzcINkHr+mxLg5xX0cvFOwbohKb3xCPSKMsCJXe4s152+pJeKAyZP60EH4fIPPSI7lrfThjSC+ZC/uhKlHiPzk7Wcbftiipgbt5tQ5DBgOa5eE3shSuCUuzjuYSvn4NHYYO+c6svSooIPnW146zqeKNiPJcgsVSaircwUTU6esiGRHxaLYuc0891K2c1Zd7VesgONPiXcBur/JCDJyOWRcJ2nAB+S9dSneRnhcIA="
    })

    request = CreateIndividualApplicationRequest(
        FullName("Jhon", "Doe"), date.today() - timedelta(days=20*365),
        Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500", "US"), "jone.doe1@unit-finance.com",
        Phone("1", "2025550108"),
        ssn=ssn,
        device_fingerprints=[device_fingerprint],
        idempotency_key=str(uuid.uuid1()),
        jwt_subject="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9fQ"
    )

    return client.applications.create(request)


def test_create_individual_application():
    app = create_individual_application()
    assert app.data.type == "individualApplication"


def create_business_application():
    request = CreateBusinessApplicationRequest(
        name="Acme Inc.",
        address=Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500", "US"),
        phone=Phone("1", "9294723497"), state_of_incorporation="CA", entity_type="Corporation", ein="123456789",
        officer=Officer(full_name=FullName("Jone", "Doe"), date_of_birth=date.today() - timedelta(days=20 * 365),
                           address=Address("950 Allerton Street", "Redwood City", "CA", "94063", "US"),
                           phone=Phone("1", "2025550108"), email="jone.doe@unit-finance.com", ssn="123456789"),
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

    return client.applications.create(request)


def test_create_business_application():
    response = create_business_application()
    assert response.data.type == "businessApplication"


def test_list_and_get_applications():
    response = client.applications.list()
    for app in response.data:
        assert app.type in ApplicationTypes
        res = client.applications.get(app.id)
        assert res.data.type in ApplicationTypes


def test_update_individual_application():
    app = create_individual_application()
    updated = client.applications.update(PatchApplicationRequest(app.data.id, tags={"patch": "test-patch"}))
    assert updated.data.type == "individualApplication"


def test_update_business_application():
    app = create_business_application()
    updated = client.applications.update(PatchApplicationRequest(app.data.id, "businessApplication",
                                                                      tags={"patch": "test-patch"}))
    assert updated.data.type == "businessApplication"


def test_cancel_individual_application():
    app = create_individual_application("000000002").data
    assert app.type == "individualApplication"
    req = CancelApplicationRequest(app.id, "By Org")
    res = client.applications.cancel(req)
    assert res.data.type == "individualApplication"
    assert res.data.id == app.id


def test_individual_application_dto():
    full_name = FullName("Jhon", "Doe")
    created_at = date.today() - timedelta(days=20 * 365)
    updated_at = date.today() - timedelta(days=20 * 365)
    address = Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500", "US"), "jone.doe1@unit-finance.com",
    phone = Phone("1", "2025550108")
    agent = Agent.from_json_api({
        "status": "Approved",
          "fullName": {
            "first": "Peter",
            "last": "Parker"
          },
          "ssn": "721074426",
          "dateOfBirth": "2001-08-15",
          "address": {
            "street": "5230 Newell Rd",
            "city": "Palo Alto",
            "state": "CA",
            "postalCode": "94303",
            "country": "US"
          },
          "phone": {
            "countryCode": "1",
            "number": "5555555555"
          },
          "email": "peter@oscorp.com"
        })

    app = IndividualApplicationDTO(id='123', created_at=created_at, full_name=full_name,
                                   address=address, date_of_birth=date(1990, 1, 1),
                                   email='johndoe@example.com', phone=phone,
                                   status="Pending", ssn='123-45-6789', message='Some message',
                                   ip='127.0.0.1', ein='12-3456789', dba='My Business', sole_proprietorship=True,
                                   tags={'tag1': 'value1', 'tag2': 'value2'},
                                   relationships={"org": {"data": {"type": "org","id": "1"}}}, archived=False,
                                   power_of_attorney_agent=agent, id_theft_score=500, industry="OtherEducationServices",
                                   passport='ABC123', nationality='US', updated_at=updated_at)

    assert app.type == "individualApplication"
    assert app.id == "123"
    assert app.attributes["address"] == address
    assert app.attributes["industry"] == "OtherEducationServices"
    assert app.attributes["powerOfAttorneyAgent"].ssn == "721074426"
    assert app.attributes["nationality"] == "US"
    assert app.attributes["passport"] == "ABC123"
    assert app.attributes["idTheftScore"] == 500


def test_create_individual_application_from_json():
    data = {
      "type": "individualApplication",
      "id": "53",
      "attributes": {
        "createdAt": "2020-01-14T14:05:04.718Z",
        "fullName": {
          "first": "Peter",
          "last": "Parker"
        },
        "ssn": "721074426",
        "address": {
          "street": "20 Ingram St",
          "street2": None,
          "city": "Forest Hills",
          "state": "NY",
          "postalCode": "11375",
          "country": "US"
        },
        "dateOfBirth": "2001-08-10",
        "email": "peter@oscorp.com",
        "phone": {
          "countryCode": "1",
          "number": "1555555578"
        },
        "status": "AwaitingDocuments",
        "message": "Waiting for you to upload the required documents.",
        "archived": False,
        "tags": {
          "userId": "106a75e9-de77-4e25-9561-faffe59d7814"
        }
      },
      "relationships": {
        "org": {
          "data": {
            "type": "org",
            "id": "1"
          }
        },
        "documents": {
          "data": [
            {
              "type": "document",
              "id": "1"
            },
            {
              "type": "document",
              "id": "2"
            }
          ]
        },
        "applicationForm": {
          "data": {
            "type": "applicationForm",
            "id": "3"
          }
        }
      }
    }

    app = IndividualApplicationDTO.from_json_api(data.get("id"), data.get("type"), data.get("attributes"),
                                                 data.get("relationships"),)

    assert app.type == "individualApplication"
    assert app.id == "53"
    assert app.attributes["ssn"] == "721074426"
    assert app.attributes["archived"] is False
    assert app.attributes["status"] == "AwaitingDocuments"


def test_business_application_dto():
    created_at = date.today() - timedelta(days=20 * 365)
    updated_at = date.today() - timedelta(days=20 * 365)
    address = Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500",
                      "US"), "jone.doe1@unit-finance.com",
    phone = Phone("1", "2025550108")

    contact = BusinessContact.from_json_api({
      "fullName": {
        "first": "Richard",
        "last": "Hendricks"
      },
      "email": "richard@piedpiper.com",
      "phone": {
        "countryCode": "1",
        "number": "1555555578"
      }
    })

    officer = Officer.from_json_api({
        "fullName": {
            "first": "Richard",
            "last": "Hendricks"
        },
        "ssn": "123456789",
        "address": {
            "street": "5230 Newell Rd",
            "street2": None,
            "city": "Palo Alto",
            "state": "CA",
            "postalCode": "94303",
            "country": "US"
        },
        "dateOfBirth": "2001-08-10",
        "email": "richard@piedpiper.com",
        "phone": {
            "countryCode": "1",
            "number": "1555555589"
        },
        "occupation": "ArchitectOrEngineer",
        "annualIncome": "Between10kAnd25k",
        "sourceOfIncome": "EmploymentOrPayrollIncome",
        "status": "Approved"
    })

    b_owner = BeneficialOwner.from_json_api([{
        "fullName": {
          "first": "Richard",
          "last": "Hendricks"
        },
        "ssn": "123456789",
        "address": {
          "street": "5230 Newell Rd",
          "street2": None,
          "city": "Palo Alto",
          "state": "CA",
          "postalCode": "94303",
          "country": "US"
        },
        "dateOfBirth": "2001-08-10",
        "phone": {
          "countryCode": "1",
          "number": "1555555589"
        },
        "email": "richard@piedpiper.com",
        "occupation": "ArchitectOrEngineer",
        "annualIncome": "Between10kAnd25k",
        "sourceOfIncome": "EmploymentOrPayrollIncome",
        "status": "Approved"
      }])

    app = BusinessApplicationDTO(id='1234', created_at=created_at, name='My Business', address=address, phone=phone,
                                 status="Pending", state_of_incorporation='CA',
                                 entity_type="Corporation", contact=contact, officer=officer,
                                 beneficial_owners=b_owner, message='Test message', ein='123456789',
                                 dba='Test DBA', tags={'tag1': 'value1', 'tag2': 'value2'},
                                 relationships={"org": {"data": {"type": "org", "id": "1"}}},
                                 updated_at=updated_at, industry="OtherEducationServices", archived=False)

    assert app.type == "businessApplication"
    assert app.id == "1234"
    assert app.attributes["address"] == address
    assert app.attributes["phone"] == phone
    assert app.attributes["status"] == "Pending"
    assert app.attributes["industry"] == "OtherEducationServices"
    assert app.attributes["dba"] == "Test DBA"
    assert app.attributes["message"] == "Test message"
    assert app.attributes["ein"] == "123456789"
    assert app.attributes["stateOfIncorporation"] == "CA"
    assert app.attributes["entityType"] == "Corporation"


def test_create_business_application_from_json():
    data = {
          "type": "businessApplication",
          "id": "50",
          "attributes": {
            "createdAt": "2020-01-13T16:01:19.346Z",
            "name": "Pied Piper",
            "dba": None,
            "address": {
              "street": "5230 Newell Rd",
              "street2": None,
              "city": "Palo Alto",
              "state": "CA",
              "postalCode": "94303",
              "country": "US"
            },
            "phone": {
              "countryCode": "1",
              "number": "1555555578"
            },
            "stateOfIncorporation": "DE",
            "ein": "123456789",
            "entityType": "Corporation",
            "contact": {
              "fullName": {
                "first": "Richard",
                "last": "Hendricks"
              },
              "email": "richard@piedpiper.com",
              "phone": {
                "countryCode": "1",
                "number": "1555555578"
              }
            },
            "officer": {
              "fullName": {
                "first": "Richard",
                "last": "Hendricks"
              },
              "ssn": "123456789",
              "address": {
                "street": "5230 Newell Rd",
                "street2": None,
                "city": "Palo Alto",
                "state": "CA",
                "postalCode": "94303",
                "country": "US"
              },
              "dateOfBirth": "2001-08-10",
              "email": "richard@piedpiper.com",
              "phone": {
                "countryCode": "1",
                "number": "1555555589"
              },
              "occupation": "ArchitectOrEngineer",
              "annualIncome": "Between10kAnd25k",
              "sourceOfIncome": "EmploymentOrPayrollIncome",
              "status": "Approved"
            },
            "beneficialOwners": [
              {
                "fullName": {
                  "first": "Richard",
                  "last": "Hendricks"
                },
                "ssn": "123456789",
                "address": {
                  "street": "5230 Newell Rd",
                  "street2": None,
                  "city": "Palo Alto",
                  "state": "CA",
                  "postalCode": "94303",
                  "country": "US"
                },
                "dateOfBirth": "2001-08-10",
                "phone": {
                  "countryCode": "1",
                  "number": "1555555589"
                },
                "email": "richard@piedpiper.com",
                "occupation": "ArchitectOrEngineer",
                "annualIncome": "Between10kAnd25k",
                "sourceOfIncome": "EmploymentOrPayrollIncome",
                "status": "Approved"
              }
            ],
            "tags": {
              "userId": "106a75e9-de77-4e25-9561-faffe59d7814"
            },
            "archived": False,
            "status": "AwaitingDocuments",
            "message": "Waiting for you to upload the required documents."
          },
          "relationships": {
            "org": {
              "data": {
                "type": "org",
                "id": "1"
              }
            },
            "documents": {
              "data": [
                {
                  "type": "document",
                  "id": "1"
                },
                {
                  "type": "document",
                  "id": "2"
                },
                {
                  "type": "document",
                  "id": "3"
                }
              ]
            },
            "applicationForm": {
              "data": {
                "type": "applicationForm",
                "id": "3"
              }
            }
          }
        }

    app = DtoDecoder.decode(data)

    assert app.type == "businessApplication"
    assert app.id == "50"
    assert app.attributes["ein"] == "123456789"
    assert app.attributes["officer"].occupation == "ArchitectOrEngineer"
    assert app.attributes["officer"].annual_income == "Between10kAnd25k"
    assert app.attributes["officer"].source_of_income == "EmploymentOrPayrollIncome"
    assert app.attributes["officer"].status == "Approved"
    assert app.attributes["beneficialOwners"][0].occupation == "ArchitectOrEngineer"
    assert app.attributes["beneficialOwners"][0].annual_income == "Between10kAnd25k"
    assert app.attributes["beneficialOwners"][0].source_of_income == "EmploymentOrPayrollIncome"
    assert app.attributes["beneficialOwners"][0].status == "Approved"
    assert app.attributes["status"] == "AwaitingDocuments"
    assert app.attributes["name"] == "Pied Piper"
    assert app.attributes["entityType"] == "Corporation"


def create_trust_application():
    request = CreateTrustApplicationRequest("Trust me Inc.", "CA", "Revocable", "Salary", "123456789",
                                            create_grantor(), create_trustee(), create_beneficiaries(),
                                            create_trust_contact(), tags={"test": "test1"})
    return client.applications.create(request)


def test_create_trust_application():
    response = create_trust_application()
    assert response.data.type == "trustApplication"
