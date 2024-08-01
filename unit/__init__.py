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
from unit.api.api_token_resource import APITokenResource
from unit.api.authorization_resource import AuthorizationResource
from unit.api.authorization_request_resource import AuthorizationRequestResource
from unit.api.account_end_of_day_resource import AccountEndOfDayResource
from unit.api.checkDeposit_resource import CheckDepositResource
from unit.api.dispute_resource import DisputeResource
from unit.api.reward_resource import RewardResource
from unit.api.recurring_payment_resource import RecurringPaymentResource
from unit.api.repayment_resource import RepaymentResource
from unit.api.check_payment_resource import CheckPaymentResource
from unit.api.tax_form_resource import TaxFormResource
from unit.utils.configuration import Configuration
from unit.api.batch_release_resource import BatchReleaseResource

__all__ = ["api", "models", "utils"]


class Unit(object):
    def __init__(self, api_url=None, token=None, retries=0, timeout=120, configuration: Configuration = None):
        if (api_url is not None or token is not None) and configuration is not None:
            raise Exception("use only configuration")

        c = configuration if configuration else Configuration(api_url, token, retries, timeout)

        self.applications = ApplicationResource(c)
        self.customers = CustomerResource(c)
        self.accounts = AccountResource(c)
        self.cards = CardResource(c)
        self.transactions = TransactionResource(c)
        self.payments = PaymentResource(c)
        self.statements = StatementResource(c)
        self.customerTokens = CustomerTokenResource(c)
        self.counterparty = CounterpartyResource(c)
        self.returnAch = ReturnAchResource(c)
        self.batchRelease = BatchReleaseResource(c)
        self.applicationForms = ApplicationFormResource(c)
        self.fees = FeeResource(c)
        self.events = EventResource(c)
        self.webhooks = WebhookResource(c)
        self.institutions = InstitutionResource(c)
        self.atmLocations = AtmLocationResource(c)
        self.api_tokens = APITokenResource(c)
        self.authorizations = AuthorizationResource(c)
        self.authorization_requests = AuthorizationRequestResource(c)
        self.account_end_of_day = AccountEndOfDayResource(c)
        self.checkDeposits = CheckDepositResource(c)
        self.disputes = DisputeResource(c)
        self.rewards = RewardResource(c)
        self.received_payments = ReceivedPaymentResource(c)
        self.repayments = RepaymentResource(c)
        self.recurring_payments = RecurringPaymentResource(c)
        self.check_payments = CheckPaymentResource(c)
        self.tax_forms = TaxFormResource(c)

