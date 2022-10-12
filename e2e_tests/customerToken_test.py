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
                                  jwt_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlZPV3VLR1R4eFlwRUNWSlAwdDRTNiJ9.eyJpc3MiOiJodHRwczovL2Rldi04NTRvbjk3dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYkpjUkQ1SHo2eWRDWXlaTDVnTjE4MXo0OGxKamFOQURAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vZGV2LTg1NG9uOTd0LnVzLmF1dGgwLmNvbS9hcGkvdjIvIiwiaWF0IjoxNjQyOTMwNDA5LCJleHAiOjE2NDMwMTY4MDksImF6cCI6ImJKY1JENUh6NnlkQ1l5Wkw1Z04xODF6NDhsSmphTkFEIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.DCF_ODpiBPhn-fcr-FF3-Ayf6fq9g8UjSqTssfvdALNxZDQMGXaQeCIisy2NLrhF81PHAX3dZzcZbpeO93OlOAomXlaVzNomEd-pCLvjv1dQoQRc2BB3IMWUxbPBdGV7kztJzIfUwrOBTNV-DqSdB4SoGYROveFa3An4Mlj2FjArTXDXhnUytq15X5p_k4zLLNzznHVd-Tdcnd7hz9sA1vvtWXu")
    response = client.customerTokens.create_token(request)
    assert response.data.type == "customerBearerToken"


def test_create_token_verification():
    account_id = create_individual_customer()
    request = CreateCustomerTokenVerification(account_id, "sms")
    response = client.customerTokens.create_token_verification(request)
    assert response.data.type == "customerTokenVerification"

