import os
import unittest
from unit import Unit
from unit.models.institution import *

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def test_institution():
    response = client.institutions.get('053285241')
    assert response.data.type == "institution"
