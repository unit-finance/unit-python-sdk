from unit.api.application_resource import ApplicationResource
from unit.api.customer_resource import CustomerResource
from unit.api.account_resource import AccountResource
from unit.api.card_resource import CardResource
from unit.api.transaction_resource import TransactionResource
from unit.api.payment_resource import PaymentResource
from unit.api.received_payment_resource import ReceivedPaymentResource
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
from unit.api.checkDeposit_resource import CheckDepositResource
from unit.api.dispute_resource import DisputeResource
from unit.api.reward_resource import RewardResource

__all__ = ["api", "models", "utils"]


class Unit(object):
    def __init__(self, api_url, token, retries=1):
        self.applications = ApplicationResource(api_url, token, retries)
        self.customers = CustomerResource(api_url, token, retries)
        self.accounts = AccountResource(api_url, token, retries)
        self.cards = CardResource(api_url, token, retries)
        self.transactions = TransactionResource(api_url, token, retries)
        self.payments = PaymentResource(api_url, token, retries)
        self.statements = StatementResource(api_url, token, retries)
        self.customerTokens = CustomerTokenResource(api_url, token, retries)
        self.counterparty = CounterpartyResource(api_url, token, retries)
        self.returnAch = ReturnAchResource(api_url, token, retries)
        self.applicationForms = ApplicationFormResource(api_url, token, retries)
        self.fees = FeeResource(api_url, token, retries)
        self.events = EventResource(api_url, token, retries)
        self.webhooks = WebhookResource(api_url, token, retries)
        self.institutions = InstitutionResource(api_url, token, retries)
        self.atmLocations = AtmLocationResource(api_url, token, retries)
        self.billPays = BillPayResource(api_url, token, retries)
        self.api_tokens = APITokenResource(api_url, token, retries)
        self.authorizations = AuthorizationResource(api_url, token, retries)
        self.authorization_requests = AuthorizationRequestResource(api_url, token, retries)
        self.account_end_of_day = AccountEndOfDayResource(api_url, token, retries)
        self.checkDeposits = CheckDepositResource(api_url, token, retries)
        self.disputes = DisputeResource(api_url, token, retries)
        self.rewards = RewardResource(api_url, token, retries)
        self.received_payments = ReceivedPaymentResource(api_url, token, retries)
