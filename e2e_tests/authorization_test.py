import os
import unittest
from unit import Unit
from unit.models.authorization import *

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def test_list_and_get_authorization_include_non_authorized():
    authorizations = client.authorizations.list()
    for authorization in authorizations.data:
        response = client.authorizations.get(authorization.id, True)
        assert response.data.type == "authorization"

def test_list_and_get_with_filter_by_status():
    params = ListAuthorizationParams(status="Authorized")
    authorizations = client.authorizations.list(params)

    for authorization in authorizations.data:
        response = client.authorizations.get(authorization.id)
        assert response.data.attributes["status"] == "Authorized"

def test_list_with_non_authorized():
    params = ListAuthorizationParams(include_non_authorized=True)
    authorizations = client.authorizations.list(params)

    for authorization in authorizations.data:
        response = client.authorizations.get(authorization.id)
        assert response.data.attributes["status"] == "Authorized"

def test_list_and_get_authorization():
    authorizations = client.authorizations.list()
    for authorization in authorizations.data:
        response = client.authorizations.get(authorization.id)
        assert response.data.type == "authorization"

def test_list_with_parameters():
    params = ListAuthorizationParams(10, 0, sort="-createdAt")
    authorizations = client.authorizations.list(params)
    for authorization in authorizations.data:
        response = client.authorizations.get(authorization.id)
        assert response.data.type == "authorization"

def test_list_with_wrong_parameters():
    params = ListAuthorizationParams(10, 0, "", "-1", include_non_authorized=False)
    response = client.authorizations.list(params)
    assert response.data == []
