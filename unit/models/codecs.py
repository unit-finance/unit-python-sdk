from unit.models.applicationForm import ApplicationFormDTO
from unit.models.application import IndividualApplicationDTO, BusinessApplicationDTO, ApplicationDocumentDTO
from unit.models.account import DepositAccountDTO, AccountLimitsDTO, AccountDepositProductDTO, CreditAccountDTO
from unit.models.customer import IndividualCustomerDTO, BusinessCustomerDTO
from unit.models.card import IndividualDebitCardDTO, BusinessDebitCardDTO, IndividualVirtualDebitCardDTO,\
    BusinessVirtualDebitCardDTO, PinStatusDTO, CardLimitsDTO, BusinessCreditCardDTO, BusinessVirtualCreditCardDTO
from unit.models.received_payment import AchReceivedPaymentDTO
from unit.models.transaction import *
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

mappings = {
        "document": lambda _id, _type, attributes, relationships:
        ApplicationDocumentDTO.from_json_api(_id, _type, attributes),

        "limits": lambda _id, _type, attributes, relationships:
        decode_limits(attributes),

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

        "apiToken": lambda _id, _type, attributes, relationships:
        APITokenDTO.from_json_api(_id, _type, attributes, relationships),
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


def decode_limits(attributes: Dict):
    if "ach" in attributes.keys():
        return AccountLimitsDTO.from_json_api(attributes)
    else:
        return CardLimitsDTO.from_json_api(attributes)


def mapping_wrapper(_id, _type, attributes, relationships):
    if _type in mappings:
        return mappings[_type](_id, _type, attributes, relationships)

    if "." in _type:
        i = _type.index(".")
        _type = _type.replace(".", "")
        t = _type[0].upper() + _type[1: i] + _type[i].upper() + _type[i + 1:] + "Event"
    else:
        t = _type[0].upper() + _type[1:] + "DTO"

    if t in globals():
        return globals()[t].from_json_api(_id, _type, attributes, relationships)

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
            return json.JSONEncoder.default(self, obj)

