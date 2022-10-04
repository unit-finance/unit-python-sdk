import os
import unittest
from unit import Unit
from e2e_tests.account_test import create_individual_customer
from unit.models.customerToken import CreateCustomerToken, CreateCustomerTokenVerification

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def test_create_token():
    account_id = create_individual_customer()
    request = CreateCustomerToken(account_id, "customers accounts")
    response = client.customerTokens.create_token(request)
    assert response.data.type == "customerBearerToken"

def test_create_jwt_token():
    account_id = create_individual_customer()
    request = CreateCustomerToken(account_id, "customers accounts",
                                  jwtSubject="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9fQ")
    response = client.customerTokens.create_token(request)
    assert response.data.type == "customerBearerToken"

def test_create_token_verification():
    account_id = create_individual_customer()
    request = CreateCustomerTokenVerification(account_id, "sms")
    response = client.customerTokens.create_token_verification(request)
    assert response.data.type == "customerTokenVerification"

