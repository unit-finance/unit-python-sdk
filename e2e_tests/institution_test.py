import os
from unit import Unit

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def test_institution():
    response = client.institutions.get('053285241')
    assert response.data.type == "institution"
