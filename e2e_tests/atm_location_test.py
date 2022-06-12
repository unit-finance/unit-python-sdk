import os
import unittest
from unit import Unit
from unit.models.atm_location import *

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def test_get_atm_location_by_coordinates():
    request = GetAtmLocationParams(30, Coordinates(-73.93041, 42.79894))
    response = client.atmLocations.get(request)
    for atm_location in response.data:
        assert atm_location.type == "atmLocation"

def test_get_atm_location_by_postal_code():
    request = GetAtmLocationParams(5, postal_code='12300')
    response = client.atmLocations.get(request)
    for atm_location in response.data:
        assert atm_location.type == "atmLocation"

def test_get_atm_location_by_address():
    request = GetAtmLocationParams(5, address=Address("1240 EASTERN AVE", "SCHENECTADY", "NY", "", "US"))
    response = client.atmLocations.get(request)
    for atm_location in response.data:
        assert atm_location.type == "atmLocation"

