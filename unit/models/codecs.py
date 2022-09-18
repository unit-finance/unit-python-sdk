from unit.models.applicationForm import ApplicationFormDTO
from unit.models.application import IndividualApplicationDTO, BusinessApplicationDTO, ApplicationDocumentDTO
from unit.models.account import DepositAccountDTO, AccountLimitsDTO, AccountDepositProductDTO, CreditAccountDTO
from unit.models.customer import IndividualCustomerDTO, BusinessCustomerDTO
from unit.models.card import IndividualDebitCardDTO, BusinessDebitCardDTO, IndividualVirtualDebitCardDTO,\
    BusinessVirtualDebitCardDTO, PinStatusDTO, CardLimitsDTO, BusinessCreditCardDTO, BusinessVirtualCreditCardDTO
from unit.models.transaction import *
from unit.models.payment import AchPaymentDTO, BookPaymentDTO, WirePaymentDTO, AchReceivedPaymentDTO
from unit.models.payment import AchPaymentDTO, BookPaymentDTO, WirePaymentDTO, BillPaymentDTO
from unit.models.customerToken import CustomerTokenDTO, CustomerVerificationTokenDTO
from unit.models.fee import FeeDTO
from unit.models.event import *
from unit.models.counterparty import CounterpartyDTO, CounterpartyBalanceDTO
from unit.models.webhook import WebhookDTO
from unit.models.institution import InstitutionDTO
from unit.models.statement import StatementDTO
from unit.models.atm_location import AtmLocationDTO
from unit.models.bill_pay import BillerDTO
from unit.models.api_token import APITokenDTO
from unit.models.authorization import AuthorizationDTO
from unit.models.authorization_request import PurchaseAuthorizationRequestDTO
from unit.models.account_end_of_day import AccountEndOfDayDTO
from unit.models.check_deposit import CheckDepositDTO
from unit.models.dispute import DisputeDTO


class DecodeLimits(object):
    @staticmethod
    def from_json_api(_id, _type, attributes, _relationships):
        if "ach" in attributes.keys():
            return AccountLimitsDTO.from_json_api(attributes)
        else:
            return CardLimitsDTO.from_json_api(attributes)


mappings = {
        "individualApplication": IndividualApplicationDTO,
        "businessApplication": BusinessApplicationDTO,
        "document": ApplicationDocumentDTO,
        "individualCustomer": IndividualCustomerDTO,
        "businessCustomer": BusinessCustomerDTO,
        "depositAccount": DepositAccountDTO,
        "creditAccount": CreditAccountDTO,
        "limits": DecodeLimits,
        "individualDebitCard": IndividualDebitCardDTO,
        "businessDebitCard": BusinessDebitCardDTO,
        "businessCreditCard": BusinessCreditCardDTO,
        "individualVirtualDebitCard": IndividualVirtualDebitCardDTO,
        "businessVirtualDebitCard": BusinessVirtualDebitCardDTO,
        "businessVirtualCreditCard": BusinessVirtualCreditCardDTO,
        "originatedAchTransaction": OriginatedAchTransactionDTO,
        "receivedAchTransaction": ReceivedAchTransactionDTO,
        "returnedAchTransaction": ReturnedAchTransactionDTO,
        "returnedReceivedAchTransaction": ReturnedReceivedAchTransactionDTO,
        "dishonoredAchTransaction": DishonoredAchTransactionDTO,
        "bookTransaction": BookTransactionDTO,
        "purchaseTransaction": PurchaseTransactionDTO,
        "atmTransaction": AtmTransactionDTO,
        "feeTransaction": FeeTransactionDTO,
        "cardTransaction": CardTransactionDTO,
        "wireTransaction": WireTransactionDTO,
        "releaseTransaction": ReleaseTransactionDTO,
        "adjustmentTransaction": AdjustmentTransactionDTO,
        "interestTransaction": InterestTransactionDTO,
        "disputeTransaction": DisputeTransactionDTO,
        "checkDepositTransaction": CheckDepositTransactionDTO,
        "returnedCheckDepositTransaction": ReturnedCheckDepositTransactionDTO,
        "paymentAdvanceTransaction": PaymentAdvanceTransactionDTO,
        "repaidPaymentAdvanceTransaction": RepaidPaymentAdvanceTransactionDTO,
        "rewardTransaction": RewardTransactionDTO,
        "paymentCanceledTransaction": PaymentCanceledTransactionDTO,
        "chargebackTransaction": ChargebackTransactionDTO,
        "cardReversalTransaction": CardReversalTransactionDTO,
        "achPayment": AchPaymentDTO,
        "bookPayment": BookPaymentDTO,
        "wirePayment": WirePaymentDTO,
        "billPayment": BillPaymentDTO,
        "achReceivedPayment": AchReceivedPaymentDTO,
        "accountStatementDTO": StatementDTO,
        "sandboxAccountStatement": StatementDTO,
        "customerBearerToken": CustomerTokenDTO,
        "customerTokenVerification": CustomerVerificationTokenDTO,
        "achCounterparty": CounterpartyDTO,
        "applicationForm": ApplicationFormDTO,
        "fee": FeeDTO,
        "account.closed": AccountClosedEvent,
        "account.frozen": AccountFrozenEvent,
        "application.awaitingDocuments": ApplicationAwaitingDocumentsEvent,
        "application.denied": ApplicationDeniedEvent,
        "application.pendingReview": ApplicationPendingReviewEvent,
        "card.activated": CardActivatedEvent,
        "card.statusChanged": CardStatusChangedEvent,
        "authorization.created": AuthorizationCreatedEvent,
        "authorizationRequest.declined": AuthorizationRequestDeclinedEvent,
        "authorizationRequest.pending": AuthorizationRequestPendingEvent,
        "authorizationRequest.approved": AuthorizationRequestApprovedEvent,
        "document.approved": DocumentApprovedEvent,
        "document.rejected": DocumentRejectedEvent,
        "document.approved": DocumentApprovedEvent,
        "checkDeposit.created": CheckDepositCreatedEvent,
        "checkDeposit.clearing": CheckDepositClearingEvent,
        "checkDeposit.sent": CheckDepositSentEvent,
        "payment.clearing": PaymentClearingEvent,
        "payment.sent": PaymentSentEvent,
        "payment.returned": PaymentReturnedEvent,
        "statements.created": StatementsCreatedEvent,
        "transaction.created": TransactionCreatedEvent,
        "customer.created": CustomerCreatedEvent,
        "account.reopened": AccountReopenedEvent,
        "webhook": WebhookDTO,
        "institution": InstitutionDTO,
        "atmLocation": AtmLocationDTO,
        "biller": BillerDTO,
        "apiToken": APITokenDTO,
        "authorization": AuthorizationDTO,
        "purchaseAuthorizationRequest": PurchaseAuthorizationRequestDTO,
        "accountEndOfDay": AccountEndOfDayDTO,
        "counterpartyBalance": CounterpartyBalanceDTO,
        "pinStatus": PinStatusDTO,
        "accountDepositProduct": AccountDepositProductDTO,
        "checkDeposit": CheckDepositDTO,
        "dispute": DisputeDTO,
    }


def split_json_api_single_response(payload: Dict):
    _id, _type, attributes = payload.get("id"), payload["type"], payload["attributes"]
    relationships = None

    if payload.get("relationships"):
        relationships = dict()
        for k, v in payload.get("relationships").items():
            if isinstance(v["data"], list):
                relationships[k] = RelationshipArray(v["data"])
            else:
                relationships[k] = Relationship(v["data"]["type"], v["data"]["id"])

    return _id, _type, attributes, relationships


def split_json_api_array_response(payload):
    if not isinstance(payload, list):
        raise Exception("split_json_api_array_response - couldn't parse response.")

    dtos = []
    for single_obj in payload:
        dtos.append(split_json_api_single_response(single_obj))

    return dtos


def mapping_wraper(_id, _type, attributes, relationships):
    if _type in mappings:
        return mappings[_type].from_json_api(_id, _type, attributes, relationships)
    else:
        return RawUnitObject(_id, _type, attributes, relationships)


class DtoDecoder(object):
    @staticmethod
    def decode(payload):
        if payload is None:
            return None
        # if response contains a list of dtos
        if isinstance(payload, list):
            dtos = split_json_api_array_response(payload)
            response = []
            for _id, _type, attributes, relationships in dtos:
                response.append(mapping_wraper(_id, _type, attributes, relationships))

            return response
        else:
            _id, _type, attributes, relationships = split_json_api_single_response(payload)
            return mapping_wraper(_id, _type, attributes, relationships)

class UnitEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)

