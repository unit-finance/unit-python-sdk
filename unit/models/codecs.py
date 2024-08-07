import json
from datetime import datetime, date
from typing import Dict

from unit.models import BeneficialOwnerDTO, RelationshipArray, Relationship, RawUnitObject
from unit.models.applicationForm import ApplicationFormDTO
from unit.models.application import IndividualApplicationDTO, BusinessApplicationDTO, ApplicationDocumentDTO
from unit.models.account import DepositAccountDTO, AccountDepositProductDTO, CreditAccountDTO, \
    CreditAccountLimitsDTO, DepositAccountLimitsDTO
from unit.models.check_payment import CheckPaymentDTO
from unit.models.batch_release import BatchReleaseDTO
from unit.models.customer import IndividualCustomerDTO, BusinessCustomerDTO
from unit.models.card import IndividualDebitCardDTO, BusinessDebitCardDTO, IndividualVirtualDebitCardDTO, \
    BusinessVirtualDebitCardDTO, PinStatusDTO, CardLimitsDTO, BusinessCreditCardDTO, BusinessVirtualCreditCardDTO, \
    MobileWalletPayloadDTO, CardToCardPaymentDTO
from unit.models.received_payment import AchReceivedPaymentDTO
from unit.models.repayment import BookRepaymentDTO, AchRepaymentDTO
from unit.models.tax_form import TaxFormDTO
from unit.models.transaction import transactions_mapper, ReturnedCheckPaymentTransactionDTO, CheckPaymentTransactionDTO
from unit.models.payment import AchPaymentDTO, BookPaymentDTO, WirePaymentDTO, AchReceivedPaymentDTO, \
    RecurringCreditAchPaymentDTO, RecurringCreditBookPaymentDTO, RecurringDebitAchPaymentDTO, BulkPaymentsDTO
from unit.models.customerToken import CustomerTokenDTO, CustomerVerificationTokenDTO
from unit.models.fee import FeeDTO
from unit.models.event import events_mapper
from unit.models.counterparty import CounterpartyDTO, CounterpartyBalanceDTO
from unit.models.webhook import WebhookDTO
from unit.models.institution import InstitutionDTO
from unit.models.statement import StatementDTO
from unit.models.atm_location import AtmLocationDTO
from unit.models.api_token import APITokenDTO
from unit.models.authorization import AuthorizationDTO
from unit.models.authorization_request import PurchaseAuthorizationRequestDTO, CardTransactionAuthorizationRequestDTO, \
    AtmAuthorizationRequestDTO
from unit.models.account_end_of_day import AccountEndOfDayDTO
from unit.models.check_deposit import CheckDepositDTO
from unit.models.dispute import DisputeDTO
from unit.utils import to_relationships

mappings = {
        "individualApplication": lambda _id, _type, attributes, relationships:
        IndividualApplicationDTO.from_json_api(_id, _type, attributes, relationships),

        "businessApplication": lambda _id, _type, attributes, relationships:
        BusinessApplicationDTO.from_json_api(_id, _type, attributes, relationships),

        "document": lambda _id, _type, attributes, relationships:
        ApplicationDocumentDTO.from_json_api(_id, _type, attributes),

        "individualCustomer": lambda _id, _type, attributes, relationships:
        IndividualCustomerDTO.from_json_api(_id, _type, attributes, relationships),

        "businessCustomer": lambda _id, _type, attributes, relationships:
        BusinessCustomerDTO.from_json_api(_id, _type, attributes, relationships),

        "depositAccount": lambda _id, _type, attributes, relationships:
        DepositAccountDTO.from_json_api(_id, _type, attributes, relationships),

        "creditAccount": lambda _id, _type, attributes, relationships:
        CreditAccountDTO.from_json_api(_id, _type, attributes, relationships),

        "limits": lambda _id, _type, attributes, relationships:
        decode_limits(_id, _type, attributes),

        "creditLimits": lambda _id, _type, attributes, relationships:
        CreditAccountLimitsDTO.from_json_api(_id, _type, attributes),

        "individualDebitCard": lambda _id, _type, attributes, relationships:
        IndividualDebitCardDTO.from_json_api(_id, _type, attributes, relationships),

        "businessDebitCard": lambda _id, _type, attributes, relationships:
        BusinessDebitCardDTO.from_json_api(_id, _type, attributes, relationships),

        "businessCreditCard": lambda _id, _type, attributes, relationships:
        BusinessCreditCardDTO.from_json_api(_id, _type, attributes, relationships),

        "individualVirtualDebitCard": lambda _id, _type, attributes, relationships:
        IndividualVirtualDebitCardDTO.from_json_api(_id, _type, attributes, relationships),

        "businessVirtualDebitCard": lambda _id, _type, attributes, relationships:
        BusinessVirtualDebitCardDTO.from_json_api(_id, _type, attributes, relationships),

        "businessVirtualCreditCard": lambda _id, _type, attributes, relationships:
        BusinessVirtualCreditCardDTO.from_json_api(_id, _type, attributes, relationships),

        "achPayment": lambda _id, _type, attributes, relationships:
        AchPaymentDTO.from_json_api(_id, _type, attributes, relationships),

        "bookPayment": lambda _id, _type, attributes, relationships:
        BookPaymentDTO.from_json_api(_id, _type, attributes, relationships),

        "wirePayment": lambda _id, _type, attributes, relationships:
        WirePaymentDTO.from_json_api(_id, _type, attributes, relationships),

        "achReceivedPayment": lambda _id, _type, attributes, relationships:
        AchReceivedPaymentDTO.from_json_api(_id, _type, attributes, relationships),

        "recurringCreditAchPayment": lambda _id, _type, attributes, relationships:
        RecurringCreditAchPaymentDTO.from_json_api(_id, _type, attributes, relationships),

        "recurringCreditBookPayment": lambda _id, _type, attributes, relationships:
        RecurringCreditBookPaymentDTO.from_json_api(_id, _type, attributes, relationships),

        "recurringDebitAchPayment": lambda _id, _type, attributes, relationships:
        RecurringDebitAchPaymentDTO.from_json_api(_id, _type, attributes, relationships),

        "bulkPayments": lambda _id, _type, attributes, relationships:
        BulkPaymentsDTO.from_json_api(_type, attributes),

        "accountStatementDTO": lambda _id, _type, attributes, relationships:
        StatementDTO.from_json_api(_id, _type, attributes, relationships),

        "sandboxAccountStatement": lambda _id, _type, attributes, relationships:
        StatementDTO.from_json_api(_id, _type, attributes, relationships),

        "customerBearerToken": lambda _id, _type, attributes, relationships:
        CustomerTokenDTO.from_json_api(_id, _type, attributes, relationships),

        "customerTokenVerification": lambda _id, _type, attributes, relationships:
        CustomerVerificationTokenDTO.from_json_api(_id, _type, attributes, relationships),

        "achCounterparty": lambda _id, _type, attributes, relationships:
        CounterpartyDTO.from_json_api(_id, _type, attributes, relationships),

        "applicationForm": lambda _id, _type, attributes, relationships:
        ApplicationFormDTO.from_json_api(_id, _type, attributes, relationships),

        "fee": lambda _id, _type, attributes, relationships:
        FeeDTO.from_json_api(_id, _type, attributes, relationships),

        "webhook": lambda _id, _type, attributes, relationships:
        WebhookDTO.from_json_api(_id, _type, attributes, relationships),

        "institution": lambda _id, _type, attributes, relationships:
        InstitutionDTO.from_json_api(_id, _type, attributes, relationships),

        "atmLocation": lambda _id, _type, attributes, relationships:
        AtmLocationDTO.from_json_api(_type, attributes),

        "apiToken": lambda _id, _type, attributes, relationships:
        APITokenDTO.from_json_api(_id, _type, attributes, relationships),

        "authorization": lambda _id, _type, attributes, relationships:
        AuthorizationDTO.from_json_api(_id, _type, attributes, relationships),

        "purchaseAuthorizationRequest": lambda _id, _type, attributes, relationships:
        PurchaseAuthorizationRequestDTO.from_json_api(_id, _type, attributes, relationships),

        "cardTransactionAuthorizationRequest": lambda _id, _type, attributes, relationships:
        CardTransactionAuthorizationRequestDTO.from_json_api(_id, _type, attributes, relationships),

        "atmAuthorizationRequest": lambda _id, _type, attributes, relationships:
        AtmAuthorizationRequestDTO.from_json_api(_id, _type, attributes, relationships),

        "accountEndOfDay": lambda _id, _type, attributes, relationships:
        AccountEndOfDayDTO.from_json_api(_id, _type, attributes, relationships),

        "counterpartyBalance": lambda _id, _type, attributes, relationships:
        CounterpartyBalanceDTO.from_json_api(_id, _type, attributes, relationships),

        "pinStatus": lambda _id, _type, attributes, relationships:
        PinStatusDTO.from_json_api(attributes),

        "accountDepositProduct": lambda _id, _type, attributes, relationships:
        AccountDepositProductDTO.from_json_api(attributes),

        "checkDeposit": lambda _id, _type, attributes, relationships:
        CheckDepositDTO.from_json_api(_id, _type, attributes, relationships),

        "dispute": lambda _id, _type, attributes, relationships:
        DisputeDTO.from_json_api(_id, _type, attributes, relationships),

        "mobileWalletPayload": lambda _id, _type, attributes, relationships:
        MobileWalletPayloadDTO.from_json_api(_id, _type, attributes, relationships),

        "bookRepayment": lambda _id, _type, attributes, relationships:
        BookRepaymentDTO.from_json_api(_id, _type, attributes, relationships),

        "achRepayment": lambda _id, _type, attributes, relationships:
        AchRepaymentDTO.from_json_api(_id, _type, attributes, relationships),

        "astra": lambda _id, _type, attributes, relationships:
        CardToCardPaymentDTO.from_json_api(_id, _type, attributes, relationships),

        "beneficialOwner": lambda _id, _type, attributes, relationships:
        BeneficialOwnerDTO.from_json_api(_id, _type, attributes, relationships),

        "checkPayment": lambda _id, _type, attributes, relationships:
        CheckPaymentDTO.from_json_api(_id, _type, attributes, relationships),

        "taxForm": lambda _id, _type, attributes, relationships:
        TaxFormDTO.from_json_api(_id, _type, attributes, relationships),

        "batchRelease": lambda _id, _type, attributes, relationships:
        BatchReleaseDTO.from_json_api(_id, _type, attributes, relationships)
    }


def split_json_api_single_response(payload: Dict):
    _id, _type, attributes = payload.get("id"), payload["type"], payload["attributes"]
    relationships = to_relationships(payload.get("relationships"))
    return _id, _type, attributes, relationships


def split_json_api_array_response(payload):
    if not isinstance(payload, list):
        raise Exception("split_json_api_array_response - couldn't parse response.")

    dtos = []
    for single_obj in payload:
        dtos.append(split_json_api_single_response(single_obj))

    return dtos


def decode_limits(_id: str, _type: str, attributes: Dict):
    if "ach" in attributes.keys():
        return DepositAccountLimitsDTO.from_json_api(_id, _type, attributes)
    else:
        return CardLimitsDTO.from_json_api(attributes)


def mapping_wrapper(_id, _type, attributes, relationships):
    if _type in mappings:
        return mappings[_type](_id, _type, attributes, relationships)
    if "." in _type:
        return events_mapper(_id, _type, attributes, relationships)
    if "Transaction" in _type:
        return transactions_mapper(_id, _type, attributes, relationships)
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
                response.append(mapping_wrapper(_id, _type, attributes, relationships))

            return response
        else:
            _id, _type, attributes, relationships = split_json_api_single_response(payload)
            return mapping_wrapper(_id, _type, attributes, relationships)


class UnitEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        else:
            try:
                return json.JSONEncoder.default(self, obj)
            except TypeError:
                return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)

