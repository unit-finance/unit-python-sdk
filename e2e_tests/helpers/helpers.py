import uuid

from unit.models import Relationship, Address, Phone, FullName


def create_relationship(_type: str, _id: str, relation: str = None):
    relation = relation or _type
    return {relation: Relationship(_type, _id)}


def generate_uuid():
    return str(uuid.uuid1())


address = Address.from_json_api({
                "street": "5230 Newell Rd",
                "street2": None,
                "city": "Palo Alto",
                "state": "CA",
                "postalCode": "94303",
                "country": "US"
            })

phone = Phone.from_json_api({
                "countryCode": "1",
                "number": "5555555555"
            })

full_name = FullName.from_json_api({
        "first": "Richard",
        "last": "Hendricks"
    })
