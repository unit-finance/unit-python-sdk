import os
import unittest
from datetime import datetime, date, timedelta
from api.unit import Unit
from models.application import *


class ApplicationE2eTests(unittest.TestCase):
    # def test_create_individual_application(self):
    #     token = os.environ.get("token")
    #     request = CreateIndividualApplicationRequest(
    #         FullName("Jhon", "Doe"), date.today() - timedelta(days=20*365),
    #         Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500", "US"), "jone.doe1@unit-finance.com",
    #         Phone("1", "2025550108"),
    #         ssn="000000002"
    #     )
    #
    #     client = Unit("https://api.s.unit.sh", token)
    #     response = client.applications.create(request)
    #     print(response)
    #     self.assertTrue(response.data.type == "individualApplication")

    def test_list_application_documents(self):
        token = os.environ.get("token")
        response = client.applications.list_documents("72996")
        print(response)
        self.assertTrue(response.data.type == "individualApplication")

