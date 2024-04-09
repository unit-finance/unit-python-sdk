from unit.utils import date_utils
from unit.models import *


class BaseTransactionDTO(object):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.attributes = {"createdAt": created_at, "direction": direction, "amount": amount, "balance": balance,
                           "summary": summary, "tags": tags}
        self.relationships = relationships


class OriginatedAchTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, description: str, addenda: Optional[str], counterparty: Counterparty,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'originatedAchTransaction'
        self.attributes["description"] = description
        self.attributes["addenda"] = addenda
        self.attributes["counterparty"] = counterparty

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return OriginatedAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["description"],
            attributes.get("addenda"), Counterparty.from_json_api(attributes["counterparty"]),
            attributes.get("tags"), relationships)


class ReceivedAchTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, description: str, addenda: Optional[str], company_name: str,
                 counterparty_routing_number: str, trace_number: Optional[str], sec_code: Optional[str],
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'receivedAchTransaction'
        self.attributes["description"] = description
        self.attributes["addenda"] = addenda
        self.attributes["companyName"] = company_name
        self.attributes["counterpartyRoutingNumber"] = counterparty_routing_number
        self.attributes["traceNumber"] = trace_number
        self.attributes["secCode"] = sec_code

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReceivedAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["description"],
            attributes.get("addenda"), attributes["companyName"], attributes["counterpartyRoutingNumber"],
            attributes.get("traceNumber"), attributes.get("secCode"), attributes.get("tags"), relationships)


class ReturnedAchTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, company_name: str, counterparty_name: str, counterparty_routing_number: str, reason: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'returnedAchTransaction'
        self.attributes["companyName"] = company_name
        self.attributes["counterpartyName"] = counterparty_name
        self.attributes["counterpartyRoutingNumber"] = counterparty_routing_number
        self.attributes["reason"] = reason

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReturnedAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"], attributes["amount"],
            attributes["balance"], attributes["summary"], attributes["companyName"], attributes["counterpartyName"],
            attributes["counterpartyRoutingNumber"], attributes["reason"], attributes.get("tags"), relationships)


class ReturnedReceivedAchTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 company_name: str, reason: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'returnedReceivedAchTransaction'
        self.attributes["companyName"] = company_name
        self.attributes["reason"] = reason

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReturnedReceivedAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["companyName"],
            attributes["reason"], attributes.get("tags"), relationships)


class DishonoredAchTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 company_name: str, counterparty_routing_number: str, reason: str, trace_number: Optional[str],
                 sec_code: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'dishonoredAchTransaction'
        self.attributes["companyName"] = company_name
        self.attributes["counterpartyRoutingNumber"] = counterparty_routing_number
        self.attributes["traceNumber"] = trace_number
        self.attributes["reason"] = reason
        self.attributes["secCode"] = sec_code

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DishonoredAchTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["companyName"],
            attributes["counterpartyRoutingNumber"], attributes["reason"], attributes.get("traceNumber"),
            attributes.get("secCode"), attributes.get("tags"), relationships)


class BookTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, counterparty: Counterparty, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'bookTransaction'
        self.attributes["counterparty"] = counterparty

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BookTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"],
            Counterparty.from_json_api(attributes["counterparty"]), attributes.get("tags"), relationships)


class PurchaseTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, card_last_4_digits: str, merchant: Merchant, coordinates: Optional[Coordinates],
                 recurring: bool, interchange: Optional[int], ecommerce: bool, card_present: bool,
                 payment_method: Optional[str], digital_wallet: Optional[str], card_verification_data,
                 card_network: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]], gross_interchange: Optional[str],
                 cash_withdrawal_amount: Optional[int], currency_conversion: Optional[CurrencyConversion],
                 rich_merchant_data: Optional[RichMerchantData]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'purchaseTransaction'
        self.attributes["cardLast4Digits"] = card_last_4_digits
        self.attributes["merchant"] = merchant
        self.attributes["coordinates"] = coordinates
        self.attributes["recurring"] = recurring
        self.attributes["interchange"] = interchange
        self.attributes["ecommerce"] = ecommerce
        self.attributes["cardPresent"] = card_present
        self.attributes["paymentMethod"] = payment_method
        self.attributes["digitalWallet"] = digital_wallet
        self.attributes["cardVerificationData"] = card_verification_data
        self.attributes["cardNetwork"] = card_network
        self.attributes["grossInterchange"] = gross_interchange
        self.attributes["cashWithdrawalAmount"] = cash_withdrawal_amount
        self.attributes["currencyConversion"] = currency_conversion
        self.attributes["richMerchantData"] = rich_merchant_data

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PurchaseTransactionDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
            attributes["amount"], attributes["balance"], attributes["summary"], attributes["cardLast4Digits"],
            Merchant.from_json_api(attributes["merchant"]), Coordinates.from_json_api(attributes.get("coordinates")),
            attributes["recurring"], attributes.get("interchange"), attributes.get("ecommerce"),
            attributes.get("cardPresent"), attributes.get("paymentMethod"), attributes.get("digitalWallet"),
            attributes.get("cardVerificationData"), attributes.get("cardNetwork"), attributes.get("tags"),
            relationships, attributes.get("grossInterchange"), attributes.get("cashWithdrawalAmount"),
            CurrencyConversion.from_json_api(attributes.get("currencyConversion")),
            RichMerchantData.from_json_api(attributes.get("richMerchantData")))


class AtmTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, card_last_4_digits: str, atm_name: str, atm_location: Optional[str], surcharge: int,
                 interchange: Optional[int], card_network: Optional[str],
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]],
                 gross_interchange: Optional[str], currency_conversion: Optional[CurrencyConversion]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'atmTransaction'
        self.attributes["cardLast4Digits"] = card_last_4_digits
        self.attributes["atmName"] = atm_name
        self.attributes["atmLocation"] = atm_location
        self.attributes["surcharge"] = surcharge
        self.attributes["interchange"] = interchange
        self.attributes["cardNetwork"] = card_network
        self.attributes["grossInterchange"] = gross_interchange
        self.attributes["currencyConversion"] = currency_conversion

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AtmTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                 attributes["amount"], attributes["balance"], attributes["summary"],
                                 attributes["cardLast4Digits"], attributes["atmName"], attributes.get("atmLocation"),
                                 attributes["surcharge"], attributes.get("interchange"), attributes.get("cardNetwork"),
                                 attributes.get("tags"), relationships, attributes.get("grossInterchange"),
                                 CurrencyConversion.from_json_api(attributes.get("currencyConversion")))


class FeeTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'feeTransaction'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return FeeTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                 attributes["amount"], attributes["balance"], attributes["summary"],
                                 attributes.get("tags"), relationships)


class CardTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, card_last_4_digits: str, merchant: Optional[Merchant], recurring: Optional[bool],
                 interchange: Optional[int], payment_method: Optional[str], digital_wallet: Optional[str],
                 card_verification_data: Optional[Dict], card_network: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]], gross_interchange: Optional[str],
                 currency_conversion: Optional[CurrencyConversion], rich_merchant_data: Optional[RichMerchantData]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'cardTransaction'
        self.attributes["cardLast4Digits"] = card_last_4_digits
        self.attributes["merchant"] = merchant
        self.attributes["recurring"] = recurring
        self.attributes["interchange"] = interchange
        self.attributes["paymentMethod"] = payment_method
        self.attributes["digitalWallet"] = digital_wallet
        self.attributes["cardVerificationData"] = card_verification_data
        self.attributes["cardNetwork"] = card_network
        self.attributes["grossInterchange"] = gross_interchange
        self.attributes["currencyConversion"] = currency_conversion
        self.attributes["richMerchantData"] = rich_merchant_data

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                  attributes["amount"], attributes["balance"], attributes["summary"],
                                  attributes["cardLast4Digits"], Merchant.from_json_api(attributes.get("merchant")),
                                  attributes.get("recurring"), attributes.get("interchange"),
                                  attributes.get("paymentMethod"), attributes.get("digitalWallet"),
                                  attributes.get("cardVerificationData"), attributes.get("cardNetwork"),
                                  attributes.get("tags"), relationships, attributes.get("grossInterchange"),
                                  CurrencyConversion.from_json_api(attributes.get("currencyConversion")),
                                  RichMerchantData.from_json_api(attributes.get("richMerchantData"))
                                  )


class CardReversalTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, card_last_4_digits: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'cardReversalTransaction'
        self.attributes["cardLast4Digits"] = card_last_4_digits

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardReversalTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                          attributes["amount"], attributes["balance"], attributes["summary"],
                                          attributes["cardLast4Digits"], attributes.get("tags"), relationships)


class WireTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int,
                 summary: str, counterparty: Counterparty, description: Optional[str],
                 originator_to_beneficiary_information: str, sender_reference: str,
                 reference_for_beneficiary: str, beneficiary_information: str,
                 beneficiary_advice_information: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'wireTransaction'
        self.attributes["description"] = description
        self.attributes["counterparty"] = counterparty
        self.attributes["originatorToBeneficiaryInformation"] = originator_to_beneficiary_information
        self.attributes["senderReference"] = sender_reference
        self.attributes["referenceForBeneficiary"] = reference_for_beneficiary
        self.attributes["beneficiaryInformation"] = beneficiary_information
        self.attributes["beneficiaryAdviceInformation"] = beneficiary_advice_information

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return WireTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                attributes["amount"], attributes["balance"], attributes["summary"],
                                Counterparty.from_json_api(attributes["counterparty"]), attributes.get("description"),
                                attributes.get("originatorToBeneficiaryInformation"), attributes.get("senderReference"),
                                attributes.get("referenceForBeneficiary"), attributes.get("beneficiaryInformation"),
                                attributes.get("beneficiaryAdviceInformation"), attributes.get("tags"), relationships)


class ReleaseTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, sender_name: str, sender_address: Address,
                 sender_account_number: str, counterparty: Counterparty, amount: int, direction: str,
                 description: str, balance: int, summary: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'releaseTransaction'
        self.attributes["description"] = description
        self.attributes["senderName"] = sender_name
        self.attributes["senderAddress"] = sender_address
        self.attributes["senderAccountNumber"] = sender_account_number
        self.attributes["counterparty"] = counterparty

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReleaseTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["senderName"],
                                     Address.from_json_api(attributes["senderAddress"]),
                                     attributes["senderAccountNumber"],
                                     Counterparty.from_json_api(attributes["counterparty"]), attributes["amount"],
                                     attributes["direction"], attributes["description"], attributes["balance"],
                                     attributes["summary"], attributes.get("tags"), relationships)


class AdjustmentTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 description: str, tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'adjustmentTransaction'
        self.attributes["description"] = description

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AdjustmentTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                        attributes["amount"], attributes["balance"],
                                        attributes["summary"], attributes["description"], attributes.get("tags"),
                                        relationships)


class InterestTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'interestTransaction'
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return InterestTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                      attributes["amount"], attributes["balance"], attributes["summary"],
                                      attributes.get("tags"), relationships)


class DisputeTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, dispute_id: str,
                 summary: str, reason: str, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'disputeTransaction'
        self.attributes["disputeId"] = dispute_id
        self.attributes["reason"] = reason

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DisputeTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                     attributes["amount"], attributes["balance"], attributes["disputeId"],
                                     attributes["summary"], attributes["reason"], attributes.get("tags"), relationships)


class CheckDepositTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'checkDepositTransaction'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                          attributes["amount"], attributes["balance"], attributes["summary"],
                                          attributes.get("tags"), relationships)


class ReturnedCheckDepositTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 reason: str, tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'returnedCheckDepositTransaction'
        self.attributes["reason"] = reason

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReturnedCheckDepositTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]),
                                                  attributes["direction"],
                                                  attributes["amount"], attributes["balance"], attributes["summary"],
                                                  attributes["reason"], attributes.get("tags"), relationships)


class PaymentAdvanceTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'paymentAdvanceTransaction'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentAdvanceTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]),
                                            attributes["direction"], attributes["amount"], attributes["balance"],
                                            attributes["summary"], attributes.get("tags"), relationships)


class RepaidPaymentAdvanceTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'repaidPaymentAdvanceTransaction'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return RepaidPaymentAdvanceTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]),
                                                  attributes["direction"],
                                                  attributes["amount"], attributes["balance"], attributes["summary"],
                                                  attributes.get("tags"), relationships)


class RewardTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 receiver_counterparty: Counterparty, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'rewardTransaction'
        self.attributes["receiverCounterparty"] = receiver_counterparty

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return RewardTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["direction"],
                                    attributes["amount"], attributes["balance"], attributes["summary"],
                                    Counterparty.from_json_api(attributes.get("receiverCounterparty")),
                                    attributes.get("tags"), relationships)


class PaymentCanceledTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'paymentCanceledTransaction'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentCanceledTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]),
                                             attributes["direction"], attributes["amount"], attributes["balance"],
                                             attributes["summary"], attributes.get("tags"), relationships)


class ChargebackTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 counterparty: Counterparty, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'chargebackTransaction'
        self.attributes["counterparty"] = counterparty

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ChargebackTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]),
                                        attributes["direction"], attributes["amount"], attributes["balance"],
                                        attributes["summary"],
                                        Counterparty.from_json_api(attributes.get("counterparty")),
                                        attributes.get("tags"), relationships)



class AccountLowBalanceClosureTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 receiver_counterparty: Counterparty, tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'accountLowBalanceClosureTransaction'
        self.attributes["receiverCounterparty"] = receiver_counterparty

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AccountLowBalanceClosureTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]),
                                                   attributes["direction"], attributes["amount"], attributes["balance"],
                                                   attributes["summary"],
                                                   Counterparty.from_json_api(attributes.get("receiverCounterparty")),
                                                   attributes.get("tags"), relationships)


class NegativeBalanceCoverageTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'negativeBalanceCoverageTransaction'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return NegativeBalanceCoverageTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]),
                                                  attributes["direction"], attributes["amount"], attributes["balance"],
                                                  attributes["summary"], attributes.get("tags"), relationships)


class PushToCardTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'pushToCardTransaction'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PushToCardTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]),
                                        attributes["direction"], attributes["amount"], attributes["balance"],
                                        attributes["summary"], attributes.get("tags"), relationships)


class CheckPaymentTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.type = 'checkPaymentTransaction'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckPaymentTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]),
                                          attributes["direction"], attributes["amount"], attributes["balance"],
                                          attributes["summary"], attributes.get("tags"), relationships)


class ReturnedCheckPaymentTransactionDTO(BaseTransactionDTO):
    def __init__(self, id: str, created_at: datetime, direction: str, amount: int, balance: int, summary: str,
                 reason: str, tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        BaseTransactionDTO.__init__(self, id, created_at, direction, amount, balance, summary, tags, relationships)
        self.attributes["reason"] = reason
        self.type = 'returnedCheckPaymentTransaction'

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReturnedCheckPaymentTransactionDTO(_id, date_utils.to_datetime(attributes["createdAt"]),
                                                  attributes["direction"], attributes["amount"], attributes["balance"],
                                                  attributes["summary"], attributes["reason"], attributes.get("tags"),
                                                  relationships)


TransactionDTO = Union[OriginatedAchTransactionDTO, ReceivedAchTransactionDTO, ReturnedAchTransactionDTO,
                       ReturnedReceivedAchTransactionDTO, DishonoredAchTransactionDTO, BookTransactionDTO,
                       PurchaseTransactionDTO, AtmTransactionDTO, FeeTransactionDTO, CardTransactionDTO,
                       CardReversalTransactionDTO, WireTransactionDTO, ReleaseTransactionDTO, AdjustmentTransactionDTO,
                       InterestTransactionDTO, DisputeTransactionDTO, CheckDepositTransactionDTO,
                       ReturnedCheckDepositTransactionDTO, PaymentAdvanceTransactionDTO,
                       RepaidPaymentAdvanceTransactionDTO, RewardTransactionDTO, PaymentCanceledTransactionDTO,
                       ChargebackTransactionDTO, AccountLowBalanceClosureTransactionDTO,
                       NegativeBalanceCoverageTransactionDTO, PushToCardTransactionDTO, CheckPaymentTransactionDTO,
                       ReturnedCheckPaymentTransactionDTO]


def transactions_mapper(_id, _type, attributes, relationships):
    c = globals()
    c_name = _type[0].upper() + _type[1:] + "DTO"
    if c_name in c.keys():
        return c[c_name].from_json_api(_id, _type, attributes, relationships)
    else:
        return RawUnitObject(_id, _type, attributes, relationships)


class PatchTransactionRequest(BaseTransactionDTO, UnitRequest):
    def __init__(self, account_id: str, transaction_id: str, tags: Optional[Dict[str, str]] = None):
        self.account_id = account_id
        self.transaction_id = transaction_id
        self.tags = tags

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "transaction",
                "attributes": {}
            }
        }

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload


class ListTransactionParams(UnitParams):
    def __init__(self, limit: int = 100, offset: int = 0, account_id: Optional[str] = None,
                 customer_id: Optional[str] = None, query: Optional[str] = None, tags: Optional[Dict[str, str]] = None,
                 since: Optional[str] = None, until: Optional[str] = None, card_id: Optional[str] = None,
                 type: Optional[List[str]] = None, exclude_fees: Optional[bool] = None,
                 sort: Optional[Literal["createdAt", "-createdAt"]] = None, include: Optional[str] = None):
        self.limit = limit
        self.offset = offset
        self.account_id = account_id
        self.customer_id = customer_id
        self.query = query
        self.tags = tags
        self.since = since
        self.until = until
        self.card_id = card_id
        self.type = type
        self.exclude_fees = exclude_fees
        self.sort = sort
        self.include = include

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.account_id:
            parameters["filter[accountId]"] = self.account_id
        if self.query:
            parameters["filter[query]"] = self.query
        if self.tags:
            parameters["filter[tags]"] = json.dumps(self.tags)
        if self.since:
            parameters["filter[since]"] = self.since
        if self.until:
            parameters["filter[until]"] = self.until
        if self.card_id:
            parameters["filter[cardId]"] = self.card_id
        if self.type:
            for idx, type_filter in enumerate(self.type):
                parameters[f"filter[type][{idx}]"] = type_filter
        if self.exclude_fees:
            parameters["filter[excludeFees]"] = self.exclude_fees
        if self.sort:
            parameters["sort"] = self.sort
        if self.include:
            parameters["include"] = self.include
        return parameters
