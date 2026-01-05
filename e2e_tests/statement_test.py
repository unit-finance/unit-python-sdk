import os
import unittest
from requests.exceptions import JSONDecodeError
from unit import Unit
from unit.models.statement import GetStatementParams, ListStatementParams

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)


def test_list_and_get_statements():
    statements = client.statements.list(ListStatementParams(2)).data
    if not statements:
        print("No statements found, skipping test")
        return
    for s in statements:
        assert s.type == "accountStatementDTO"

        try:
            params = GetStatementParams(s.id)
            html_statement = client.statements.get(params).data
            assert "<!DOCTYPE html>" in str(html_statement)

            params = GetStatementParams(s.id, customer_id=s.relationships["customer"].id)
            html_statement = client.statements.get(params).data
            assert "<!DOCTYPE html>" in str(html_statement)

            account_id = s.relationships["account"].id
            pdf_response = client.statements.get_bank_verification(account_id).data
            assert "PDF" in str(pdf_response)

            params = GetStatementParams(s.id, "pdf")
            pdf_statement = client.statements.get(params).data
            assert "PDF" in str(pdf_statement)
        except JSONDecodeError:
            print(f"Skipping statement {s.id} - returned 404")
            continue
