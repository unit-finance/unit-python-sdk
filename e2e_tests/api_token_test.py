import os
import unittest
from datetime import datetime, timedelta
from unit import Unit
from unit.models.api_token import CreateAPITokenRequest
from unit.utils.date_utils import from_datetime

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)
user_id = "252"
expiration_time = datetime.now() + timedelta(hours=1)

def create_api_token():
    request = CreateAPITokenRequest(user_id, "Test token", "customers applications", expiration_time)
    return client.api_tokens.create(request).data

def test_list_api_tokens():
    api_tokens_ids = []
    response = client.api_tokens.list(user_id)

    for t in response.data:
        assert t.type == "apiToken"

def test_create_api_token():
    api_token = create_api_token()
    assert api_token.type == "apiToken"

def test_create_api_token_prev_version( ):
    request = CreateAPITokenRequest(user_id, "Test token", "customers applications", from_datetime(expiration_time))
    api_token = client.api_tokens.create(request).data
    assert api_token.type == "apiToken"

def test_delete_api_token():
    api_token = create_api_token()
    response = client.api_tokens.revoke(user_id, api_token.id)
    assert response.data == []
