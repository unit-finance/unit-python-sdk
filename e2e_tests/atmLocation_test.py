import os
import unittest
from unit import Unit
from unit.models.atmLocation import *

class AtmLocationE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_get_atm_location_by_coordinates(self):
        request = GetAtmLocationRequest(30, Coordinates(-73.93041, 42.79894))
        response = self.client.atmLocations.get(request)
        self.assertTrue(response.data.type == "atmLocation")

    def test_get_atm_location_by_postal_code(self):
        request = GetAtmLocationRequest(30, postal_code=12300)
        response = self.client.atmLocations.get(request)
        for atm_location in response.data:
            self.assertTrue(atm_location.type == "atmLocation")
    #
    # def test_get_atm_location_by_address(self):
    #     request = GetAtmLocationRequest(30, address=Address("1240 EASTERN AVE","SCHENECTADY","NY","","US"))
    #     response = self.client.atmLocations.get(request)
    #     print(len(response.data))
    #     for atm_location in response.data:
    #         self.assertTrue(atm_location.type == "atmLocation")


if __name__ == '__main__':
    unittest.main()

