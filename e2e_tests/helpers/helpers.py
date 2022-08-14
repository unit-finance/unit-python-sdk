from unit.models import Relationship, Grantor, TrustContact, Trustee, Beneficiary


def create_relationship(type: str, id: str, relation: str = None):
    relation = relation or type
    return {relation: Relationship(type, id)}


def create_grantor():
    return Grantor.from_json_api({
                                                "fullName": {
                                                    "first": "Laurie",
                                                    "last": "Bream"
                                                },
                                                "dateOfBirth": "2000-01-01",
                                                "ssn": "000000003",
                                                "email": "laurie@raviga.com",
                                                "phone": {
                                                    "countryCode": "1",
                                                    "number": "2025550108"
                                                },
                                                "address": {
                                                    "street": "950 Allerton Street",
                                                    "city": "Redwood City",
                                                    "state": "CA",
                                                    "postalCode": "94063",
                                                    "country": "US"
                                                }
                                            })


def create_trust_contact():
    return TrustContact.from_json_api({
        "fullName": {
          "first": "Jared",
          "last": "Dunn"
        },
        "email": "jared@piedpiper.com",
        "phone": {
          "countryCode": "1",
          "number": "2025550108"
        },
        "address": {
          "street": "5230 Newell Rd",
          "city": "Palo Alto",
          "state": "CA",
          "postalCode": "94303",
          "country": "US"
        }
      })


def create_trustee():
    return [Trustee.from_json_api({
          "fullName": {
            "first": "Richard",
            "last": "Hendricks"
          },
          "dateOfBirth": "2000-01-01",
          "ssn": "000000002",
          "email": "richard@piedpiper.com",
          "phone": {
            "countryCode": "1",
            "number": "2025550108"
          },
          "address": {
            "street": "5230 Newell Rd",
            "city": "Palo Alto",
            "state": "CA",
            "postalCode": "94303",
            "country": "US"
          }
        })]


def create_beneficiaries():
    return [
        Beneficiary.from_json_api({
          "fullName": {
            "first": "Dinesh",
            "last": "Chugtai"
          },
          "dateOfBirth": "2000-01-01"
        }),
        Beneficiary.from_json_api({
          "fullName": {
            "first": "Gilfoyle",
            "last": "Unknown"
          },
          "dateOfBirth": "2000-01-01"
        })
    ]

