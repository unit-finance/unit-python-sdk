import os
import unittest
from unit import Unit
from unit.models.institution import *

class InstitutionE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_institution(self):
        response = self.client.institutions.get('053285241')
        self.assertTrue(response.data.type == "institution")

if __name__ == '__main__':
    unittest.main()
