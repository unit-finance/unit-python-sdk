from unit.utils import date_utils
from unit.models import *


class OriginatedAchTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return OriginatedAchTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class ReceivedAchTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReceivedAchTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class ReturnedAchTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReturnedAchTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class ReturnedReceivedAchTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReturnedReceivedAchTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class DishonoredAchTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DishonoredAchTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class BookTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return BookTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class PurchaseTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PurchaseTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class AtmTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AtmTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class FeeTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return FeeTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class CardTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class CardReversalTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CardReversalTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class WireTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return WireTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class ReleaseTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReleaseTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class AdjustmentTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AdjustmentTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class InterestTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return InterestTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class DisputeTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return DisputeTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class CheckDepositTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return CheckDepositTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class ReturnedCheckDepositTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ReturnedCheckDepositTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class PaymentAdvanceTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentAdvanceTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class RepaidPaymentAdvanceTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return RepaidPaymentAdvanceTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class RewardTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return RewardTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class PaymentCanceledTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return PaymentCanceledTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


class ChargebackTransactionDTO(UnitDTO):
    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return ChargebackTransactionDTO(_id, _type, attributes_to_object(attributes), relationships)


TransactionDTO = Union[OriginatedAchTransactionDTO, ReceivedAchTransactionDTO, ReturnedAchTransactionDTO,
                       ReturnedReceivedAchTransactionDTO, DishonoredAchTransactionDTO, BookTransactionDTO,
                       PurchaseTransactionDTO, AtmTransactionDTO, FeeTransactionDTO, CardTransactionDTO,
                       CardReversalTransactionDTO, WireTransactionDTO, ReleaseTransactionDTO, AdjustmentTransactionDTO,
                       InterestTransactionDTO, DisputeTransactionDTO, CheckDepositTransactionDTO,
                       ReturnedCheckDepositTransactionDTO, PaymentAdvanceTransactionDTO,
                       RepaidPaymentAdvanceTransactionDTO, RewardTransactionDTO, PaymentCanceledTransactionDTO,
                       ChargebackTransactionDTO]


class PatchTransactionRequest(UnitRequest):
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
                 customer_id: Optional[str] = None, query: Optional[str] = None, tags: Optional[object] = None,
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
            parameters["filter[tags]"] = self.tags
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