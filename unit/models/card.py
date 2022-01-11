from unit.utils import date_utils
from unit.models import *

CardStatus = Literal["Inactive", "Active", "Stolen", "Lost", "Frozen", "ClosedByCustomer", "SuspectedFraud"]


class IndividualDebitCardDTO(object):
    def __init__(self, id: str, created_at: datetime, last_4_digits: str, expiration_date: str, status: CardStatus,
                 shipping_address: Optional[Address], design: Optional[str],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "individualDebitCard"
        self.attributes = {"createdAt": created_at, "last4Digits": last_4_digits, "expirationDate": expiration_date,
                           "status": status, "shippingAddress": shipping_address, "design": design}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        shipping_address = Address.from_json_api(attributes.get("shippingAddress")) if attributes.get("shippingAddress") else None
        return IndividualDebitCardDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["last4Digits"],
            attributes["expirationDate"], attributes["status"],
            shipping_address, attributes.get("design"), relationships
        )


class BusinessDebitCardDTO(object):
    def __init__(self, id: str, created_at: datetime, last_4_digits: str, expiration_date: str, ssn: str,
                 full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 status: CardStatus, passport: Optional[str], nationality: Optional[str],
                 shipping_address: Optional[Address], design: Optional[str],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "businessDebitCard"
        self.attributes = {"createdAt": created_at, "last4Digits": last_4_digits, "expirationDate": expiration_date,
                           "ssn": ssn, "fullName": full_name, "dateOfBirth": date_of_birth, "address": address,
                           "phone": phone, "email": email, "status": status, "passport": passport,
                           "nationality": nationality, "shippingAddress": shipping_address, "design": design}
        self.relationships = relationships

    def from_json_api(_id, _type, attributes, relationships):
        shipping_address = Address.from_json_api(attributes.get("shippingAddress")) if attributes.get("shippingAddress") else None
        return BusinessDebitCardDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["last4Digits"],
            attributes["expirationDate"], attributes["ssn"], FullName.from_json_api(attributes["fullName"]),
            attributes["dateOfBirth"], Address.from_json_api(attributes["address"]),
            Phone.from_json_api(attributes["phone"]), attributes["email"], attributes["status"],
            attributes.get("passport"), attributes.get("nationality"),
            shipping_address, attributes.get("design"), relationships
        )


class IndividualVirtualDebitCardDTO(object):
    def __init__(self, id: str, created_at: datetime, last_4_digits: str, expiration_date: str, status: CardStatus,
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "individualVirtualDebitCard"
        self.attributes = {"createdAt": created_at, "last4Digits": last_4_digits, "expirationDate": expiration_date,
                           "status": status}
        self.relationships = relationships

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        return IndividualVirtualDebitCardDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["last4Digits"],
            attributes["expirationDate"], attributes["status"], relationships
        )


class BusinessVirtualDebitCardDTO(object):
    def __init__(self, id: str, created_at: datetime, last_4_digits: str, expiration_date: str, ssn: str,
                 full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 status: CardStatus, passport: Optional[str], nationality: Optional[str],
                 relationships: Optional[Dict[str, Relationship]]):
        self.id = id
        self.type = "businessVirtualDebitCard"
        self.attributes = {"createdAt": created_at, "last4Digits": last_4_digits, "expirationDate": expiration_date,
                           "ssn": ssn, "fullName": full_name, "dateOfBirth": date_of_birth, "address": address,
                           "phone": phone, "email": email, "status": status, "passport": passport,
                           "nationality": nationality}
        self.relationships = relationships

    def from_json_api(_id, _type, attributes, relationships):
        return BusinessVirtualDebitCardDTO(
            _id, date_utils.to_datetime(attributes["createdAt"]), attributes["last4Digits"],
            attributes["expirationDate"], attributes["ssn"], FullName.from_json_api(attributes["fullName"]),
            attributes["dateOfBirth"], Address.from_json_api(attributes["address"]),
            Phone.from_json_api(attributes["phone"]), attributes["email"], attributes["status"],
            attributes.get("passport"), attributes.get("nationality"), relationships
        )


Card = Union[IndividualDebitCardDTO, BusinessDebitCardDTO, IndividualVirtualDebitCardDTO, BusinessVirtualDebitCardDTO]


class CreateIndividualDebitCard(object):
    def __init__(self, relationships: Dict[str, Relationship], shipping_address: Optional[Address] = None,
                 design: Optional[str] = None, idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None):
        self.shipping_address = shipping_address
        self.design = design
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "individualDebitCard",
                "attributes": {},
                "relationships": self.relationships
            }
        }

        if self.shipping_address:
            payload["data"]["attributes"]["shippingAddress"] = self.shipping_address

        if self.design:
            payload["data"]["attributes"]["design"] = self.design

        if self.idempotency_key:
            payload["data"]["attributes"]["idempotencyKey"] = self.idempotency_key

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())

class CreateBusinessDebitCard(object):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 status: CardStatus, shipping_address: Optional[Address], ssn: Optional[str], passport: Optional[str],
                 nationality: Optional[str], design: Optional[str], idempotency_key: Optional[str],
                 tags: Optional[Dict[str, str]], relationships: Optional[Dict[str, Relationship]]):
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone = phone
        self.email = email
        self.status = status
        self.shipping_address = shipping_address
        self.ssn = ssn
        self.passport = passport
        self.nationality = nationality
        self.design = design
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "businessDebitCard",
                "attributes": {
                    "fullName": self.full_name,
                    "dateOfBirth": self.date_of_birth,
                    "address": self.address,
                    "phone": self.phone,
                    "email": self.email,
                },
                "relationships": self.relationships
            }
        }

        if self.shipping_address:
            payload["data"]["attributes"]["shippingAddress"] = self.shipping_address

        if self.ssn:
            payload["data"]["attributes"]["ssn"] = self.ssn

        if self.passport:
            payload["data"]["attributes"]["passport"] = self.passport

        if self.nationality:
            payload["data"]["attributes"]["nationality"] = self.nationality

        if self.design:
            payload["data"]["attributes"]["design"] = self.design

        if self.idempotency_key:
            payload["data"]["attributes"]["idempotencyKey"] = self.idempotency_key

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())

class CreateIndividualVirtualDebitCard(object):
    def __init__(self, relationships: Dict[str, Relationship], idempotency_key: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None):
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "individualVirtualDebitCard",
                "attributes": {},
                "relationships": self.relationships
            }
        }

        if self.idempotency_key:
            payload["data"]["attributes"]["idempotencyKey"] = self.idempotency_key

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class CreateBusinessVirtualDebitCard(object):
    def __init__(self, full_name: FullName, date_of_birth: date, address: Address, phone: Phone, email: str,
                 status: CardStatus, ssn: Optional[str], passport: Optional[str], nationality: Optional[str],
                 idempotency_key: Optional[str], tags: Optional[Dict[str, str]],
                 relationships: Optional[Dict[str, Relationship]]):
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone = phone
        self.email = email
        self.status = status
        self.ssn = ssn
        self.passport = passport
        self.nationality = nationality
        self.idempotency_key = idempotency_key
        self.tags = tags
        self.relationships = relationships

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "businessVirtualDebitCard",
                "attributes": {
                    "fullName": self.full_name,
                    "dateOfBirth": self.date_of_birth,
                    "address": self.address,
                    "phone": self.phone,
                    "email": self.email,
                },
                "relationships": self.relationships
            }
        }

        if self.ssn:
            payload["data"]["attributes"]["ssn"] = self.ssn

        if self.passport:
            payload["data"]["attributes"]["passport"] = self.passport

        if self.nationality:
            payload["data"]["attributes"]["nationality"] = self.nationality

        if self.idempotency_key:
            payload["data"]["attributes"]["idempotencyKey"] = self.idempotency_key

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


CreateCardRequest = Union[CreateIndividualDebitCard, CreateBusinessDebitCard, CreateIndividualVirtualDebitCard,
                          CreateBusinessVirtualDebitCard]

class PatchIndividualDebitCard(object):
    def __init__(self,card_id: str, shipping_address: Optional[Address] = None, design: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None):
        self.card_id = card_id
        self.shipping_address = shipping_address
        self.design = design
        self.tags = tags

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "individualDebitCard",
                "attributes": {},
            }
        }

        if self.shipping_address:
            payload["data"]["attributes"]["shippingAddress"] = self.shipping_address

        if self.design:
            payload["data"]["attributes"]["design"] = self.design

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())


class PatchBusinessDebitCard(object):
    def __init__(self, card_id: str, shipping_address: Optional[Address] = None, address: Optional[Address] = None,
                 phone: Optional[Phone] = None, email: Optional[str] = None, design: Optional[str] = None,
                 tags: Optional[Dict[str, str]] = None):
        self.card_id = card_id
        self.shipping_address = shipping_address
        self.design = design
        self.tags = tags

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "businessDebitCard",
                "attributes": {},
            }
        }

        if self.shipping_address:
            payload["data"]["attributes"]["shippingAddress"] = self.shipping_address

        if self.address:
            payload["data"]["attributes"]["address"] = self.address

        if self.phone:
            payload["data"]["attributes"]["phone"] = self.phone

        if self.email:
            payload["data"]["attributes"]["email"] = self.email

        if self.design:
            payload["data"]["attributes"]["design"] = self.design

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())

class PatchIndividualVirtualDebitCard(object):
    def __init__(self, card_id: str, tags: Optional[Dict[str, str]] = None):
        self.card_id = card_id
        self.tags = tags

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "individualVirtualDebitCard",
                "attributes": {},
            }
        }

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())

class PatchBusinessVirtualDebitCard(object):
    def __init__(self, card_id: str, address: Optional[Address] = None, phone: Optional[Phone] = None,
                 email: Optional[str] = None, tags: Optional[Dict[str, str]] = None):
        self.card_id = card_id
        self.address = address
        self.phone = phone
        self.email = email
        self.tags = tags

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "businessVirtualDebitCard",
                "attributes": {},
            }
        }

        if self.address:
            payload["data"]["attributes"]["address"] = self.address

        if self.phone:
            payload["data"]["attributes"]["phone"] = self.phone

        if self.email:
            payload["data"]["attributes"]["email"] = self.email

        if self.tags:
            payload["data"]["attributes"]["tags"] = self.tags

        return payload

    def __repr__(self):
        json.dumps(self.to_json_api())

PatchCardRequest = Union[PatchIndividualDebitCard, PatchBusinessDebitCard, PatchIndividualVirtualDebitCard,
                         PatchBusinessVirtualDebitCard]

class ReplaceCardRequest(object):
    def __init__(self, shipping_address: Optional[Address] = None):
        self.shipping_address = shipping_address

    def to_json_api(self) -> Dict:
        payload = {
            "data": {
                "type": "replaceCard",
                "attributes": {},
            }
        }

        if self.shipping_address:
            payload["data"]["attributes"]["shippingAddress"] = self.shipping_address

        return payload

        def __repr__(self):
            json.dumps(self.to_json_api())

PinStatus = Literal["Set", "NotSet"]

class PinStatusDTO(object):
    def __init__(self, status: PinStatus):
        self.type = "pinStatus"
        self.attributes = {"status": status}

    @staticmethod
    def from_json_api(attributes):
        return PinStatusDTO(attributes["status"])


class CardLimitsDTO(object):
    def __init__(self, limits: CardLevelLimits, daily_totals: CardTotals, monthly_totals: CardTotals):
        self.type = "limits"
        self.attributes = {"limits": limits, "dailyTotals": daily_totals, "monthlyTotals": monthly_totals}

    @staticmethod
    def from_json_api(_id, _type, attributes, relationships):
        limits = CardLevelLimits.from_json_api(attributes.get("limits")) if attributes.get("limits") else None
        return CardLimitsDTO(limits, CardTotals.from_json_api(attributes.get("dailyTotals")),
                          CardTotals.from_json_api(attributes.get("monthlyTotals")))
