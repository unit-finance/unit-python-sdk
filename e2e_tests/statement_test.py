import os
import unittest
from unit import Unit
from unit.models.statement import GetStatementParams


class StatementE2eTests(unittest.TestCase):
    token = os.environ.get("token")
    client = Unit("https://api.s.unit.sh", token)

    def test_list_and_get_statements(self):
        statements = self.client.statements.list().data
        for s in statements:
            self.assertTrue(s.type == "accountStatementDTO")

            params = GetStatementParams(s.id)
            html_statement = self.client.statements.get(params).data
            self.assertTrue("<!DOCTYPE html>" in html_statement)

            params = GetStatementParams(s.id, customer_id=s.relationships["customer"].id)
            html_statement = self.client.statements.get(params).data
            self.assertTrue("<!DOCTYPE html>" in html_statement)

            account_id = s.relationships["account"].id
            pdf_response = self.client.statements.get_bank_verification(account_id).data
            self.assertTrue("PDF" in pdf_response)

            params = GetStatementParams(s.id, "pdf")
            pdf_statement = self.client.statements.get(params).data
            self.assertTrue("PDF" in pdf_statement)


if __name__ == '__main__':
    unittest.main()
