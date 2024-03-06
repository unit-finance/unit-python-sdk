import json
from typing import Optional
from unit.models import *
from unit.utils import date_utils

AuthorizationStatus = Literal["Authorized", "Completed", "Canceled", "Declined"]


class AuthorizationDTO(object):
    def __init__(self, id: str, created_at: datetime, amount: int, card_last_4_digits: str, status: AuthorizationStatus,
                 merchant_name: str,
                 merchant_type: int, merchant_category: str, merchant_location: Optional[str], recurring: bool,
                 payment_method: Optional[str], digital_wallet: Optional[str], card_verification_data,
                 card_network: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]], merchant_id: Optional[str],
                 decline_reason: Optional[str], cash_withdrawal_amount: Optional[int], rich_merchant_data: Optional[RichMerchantData]):
        self.id = id
        self.type = "authorization"
        self.attributes = {"createdAt": created_at, "amount": amount, "cardLast4Digits": card_last_4_digits,
                           "status": status, "merchant": {"name": merchant_name, "type": merchant_type,
                                                          "category": merchant_category, "location": merchant_location,
                                                          "id": merchant_id},
                           "recurring": recurring, "paymentMethod": payment_method, "digitalWallet": digital_wallet,
                           "cardVerificationData": card_verification_data, "cardNetwork": card_network, "tags": tags,
                           "declineReason": decline_reason, "cashWithdrawalAmount": cash_withdrawal_amount,
                           "richMerchantData": rich_merchant_data}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return AuthorizationDTO(_id, date_utils.to_datetime(attributes["createdAt"]), attributes["amount"],
                                attributes["cardLast4Digits"], attributes["status"], attributes["merchant"]["name"],
                                attributes["merchant"]["type"], attributes["merchant"]["category"],
                                attributes["merchant"].get("location"), attributes["recurring"],
                                attributes.get("paymentMethod"), attributes.get("digitalWallet"),
                                attributes.get("cardVerificationData"), attributes.get("cardNetwork"),
                                attributes.get("tags"), relationships, attributes["merchant"].get("id"),
                                attributes.get("declineReason"), attributes.get("cashWithdrawalAmount"))


class ListAuthorizationParams(UnitParams):
    def __init__(self, limit: int = 100, offset: int = 0, account_id: Optional[str] = None,
                 customer_id: Optional[str] = None, card_id: Optional[str] = None, since: Optional[str] = None,
                 until: Optional[str] = None, include_non_authorized: Optional[bool] = False,
                 status: Optional[str] = None, sort: Optional[Literal["createdAt", "-createdAt"]] = None):
        self.limit = limit
        self.offset = offset
        self.account_id = account_id
        self.customer_id = customer_id
        self.card_id = card_id
        self.since = since
        self.until = until
        self.include_non_authorized = include_non_authorized
        self.status = status
        self.sort = sort

    def to_dict(self) -> Dict:
        parameters = {"page[limit]": self.limit, "page[offset]": self.offset}
        if self.customer_id:
            parameters["filter[customerId]"] = self.customer_id
        if self.account_id:
            parameters["filter[accountId]"] = self.account_id
        if self.card_id:
            parameters["filter[cardId]"] = self.card_id
        if self.include_non_authorized:
            parameters["filter[includeNonAuthorized]"] = self.include_non_authorized
        if self.status:
            parameters["filter[status]"] = self.status
        if self.since:
            parameters["filter[since]"] = self.since
        if self.until:
            parameters["filter[until]"] = self.until
        if self.sort:
            parameters["sort"] = self.sort
        return parameters
