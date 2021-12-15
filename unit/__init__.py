from unit.api.application_resource import ApplicationResource
from unit.api.customer_resource import CustomerResource
from unit.api.account_resource import AccountResource
from unit.api.card_resource import CardResource
from unit.api.transaction_resource import TransactionResource
from unit.api.payment_resource import PaymentResource
from unit.api.statement_resource import StatementResource
from unit.api.customerToken_resource import CustomerTokenResource
from unit.api.counterparty_resource import CounterpartyResource
from unit.api.returnAch_resource import ReturnAchResource
from unit.api.applicationForm_resource import ApplicationFormResource
from unit.api.fee_resource import FeeResource
from unit.api.event_resource import EventResource
from unit.api.webhook_resource import WebhookResource
from unit.api.institution_resource import InstitutionResource
from unit.api.atmLocation_resource import AtmLocationResource
from unit.api.bill_pay_resource import BillPayResource
from unit.api.api_token_resource import APITokenResource
from unit.api.authorization_resource import AuthorizationResource
from unit.api.authorization_request_resource import AuthorizationRequestResource
from unit.api.account_end_of_day_resource import AccountEndOfDayResource

__all__ = ["api", "models", "utils"]


class Unit(object):
    def __init__(self, api_url, token):
        self.applications = ApplicationResource(api_url, token)
        self.customers = CustomerResource(api_url, token)
        self.accounts = AccountResource(api_url, token)
        self.cards = CardResource(api_url, token)
        self.transactions = TransactionResource(api_url, token)
        self.payments = PaymentResource(api_url, token)
        self.statements = StatementResource(api_url, token)
        self.customerTokens = CustomerTokenResource(api_url, token)
        self.counterparty = CounterpartyResource(api_url, token)
        self.returnAch = ReturnAchResource(api_url, token)
        self.applicationForms = ApplicationFormResource(api_url, token)
        self.fees = FeeResource(api_url, token)
        self.events = EventResource(api_url, token)
        self.webhooks = WebhookResource(api_url, token)
        self.institutions = InstitutionResource(api_url, token)
        self.atmLocations = AtmLocationResource(api_url, token)
        self.billPays = BillPayResource(api_url, token)
        self.api_tokens = APITokenResource(api_url, token)
        self.authorizations = AuthorizationResource(api_url, token)
        self.authorization_requests = AuthorizationRequestResource(api_url, token)
        self.account_end_of_day = AccountEndOfDayResource(api_url, token)
