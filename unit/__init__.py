from unit.api.application_resource import ApplicationResource
from unit.api.customer_resource import CustomerResource
from unit.api.account_resource import AccountResource
from unit.api.card_resource import CardResource
from unit.api.transaction_resource import TransactionResource
from unit.api.payment_resource import PaymentResource
from unit.api.customer_token_resource import CustomerTokenResource
from unit.api.counterparty_resource import CounterpartyResource
from unit.api.counterparty_resource import CounterpartyResource
from unit.api.return_ach_resource import ReturnAchResource
from unit.api.application_form_resource import ApplicationFormResource
from unit.api.fee_resource import FeeResource
from unit.api.event_resource import EventResource
from unit.api.webhook_resource import WebhookResource
from unit.api.institution_resource import InstitutionResource

__all__ = ["api", "models", "utils"]


class Unit(object):
    def __init__(self, api_url, token):
        self.applications = ApplicationResource(api_url, token)
        self.customers = CustomerResource(api_url, token)
        self.accounts = AccountResource(api_url, token)
        self.cards = CardResource(api_url, token)
        self.transactions = TransactionResource(api_url, token)
        self.payments = PaymentResource(api_url, token)
        self.customer_tokens = CustomerTokenResource(api_url, token)
        self.counterparty = CounterpartyResource(api_url, token)
        self.return_achs = ReturnAchResource(api_url, token)
        self.application_forms = ApplicationFormResource(api_url, token)
        self.fees = FeeResource(api_url, token)
        self.events = EventResource(api_url, token)
        self.webhooks = WebhookResource(api_url, token)
        self.institutions = InstitutionResource(api_url, token)
