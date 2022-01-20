import os
import unittest
from unit import Unit
from unit.models.authorization import *

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def test_list_and_get_authorization():
    authorizations = client.authorizations.list()
    for authorization in authorizations.data:
        response = client.authorizations.get(authorization.id)
        assert response.data.type == "authorization"

def test_list_with_parameters():
    params = AuthorizationListParams(10, 0, "", "49423")
    authorizations = client.authorizations.list(params)
    for authorization in authorizations.data:
        response = client.authorizations.get(authorization.id)
        assert response.data.type == "authorization"

def test_list_with_wrong_parameters():
    params = AuthorizationListParams(10, 0, "", "-1")
    response = client.authorizations.list(params)
    assert response.data == []
