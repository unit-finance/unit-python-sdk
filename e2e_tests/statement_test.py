import os
import unittest
from unit import Unit
from unit.models.statement import GetStatementParams, ListStatementParams

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def test_list_and_get_statements():
    statements = client.statements.list(ListStatementParams(2)).data
    for s in statements:
        assert s.type == "accountStatementDTO"

        params = GetStatementParams(s.id)
        html_statement = client.statements.get(params).data
        assert "<!DOCTYPE html>" in html_statement

        params = GetStatementParams(s.id, customer_id=s.relationships["customer"].id)
        html_statement = client.statements.get(params).data
        assert "<!DOCTYPE html>" in html_statement

        account_id = s.relationships["account"].id
        pdf_response = client.statements.get_bank_verification(account_id).data
        assert "PDF" in pdf_response

        params = GetStatementParams(s.id, "pdf")
        pdf_statement = client.statements.get(params).data
        assert "PDF" in pdf_statement
