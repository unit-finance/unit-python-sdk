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
from unit.api.repayment_resource import RepaymentResource

__all__ = ["api", "models", "utils"]

from unit.utils.configuration import Configuration


class Unit(object):
    def __init__(self, api_url, token, retries=1, timeout=120, configuration: Configuration = None):
        c = configuration if configuration else Configuration(api_url, token, retries, timeout)
        c.set_globals()

        self.applications = ApplicationResource()
        self.customers = CustomerResource()
        self.accounts = AccountResource()
        self.cards = CardResource()
        self.transactions = TransactionResource()
        self.payments = PaymentResource()
        self.statements = StatementResource()
        self.customerTokens = CustomerTokenResource()
        self.counterparty = CounterpartyResource()
        self.returnAch = ReturnAchResource()
        self.applicationForms = ApplicationFormResource()
        self.fees = FeeResource()
        self.events = EventResource()
        self.webhooks = WebhookResource()
        self.institutions = InstitutionResource()
        self.atmLocations = AtmLocationResource()
        self.billPays = BillPayResource()
        self.api_tokens = APITokenResource()
        self.authorizations = AuthorizationResource()
        self.authorization_requests = AuthorizationRequestResource()
        self.account_end_of_day = AccountEndOfDayResource()
        self.checkDeposits = CheckDepositResource()
        self.disputes = DisputeResource()
        self.rewards = RewardResource()
        self.received_payments = ReceivedPaymentResource()
        self.repayments = RepaymentResource()
