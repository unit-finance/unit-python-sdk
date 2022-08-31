from typing import List

from unit.models import Relationship, Counterparty, WireCounterparty, Address


def create_relationship(_type: str, _id: str, relation: str = None):
    relation = relation or _type
    return {relation: Relationship(_type, _id)}


def create_relationships_dict(relationships: List[Relationship]):
    d = {}

    for r in relationships:
        d.update(r)

    return d


def create_counterparty_dto(routing_number: str, account_number: str, account_type: str, name: str):
    return Counterparty(routing_number, account_number, account_type, name)


def create_wire_counterparty_dto(routing_number: str, account_number: str, name: str, address: Address):
    return WireCounterparty(routing_number, account_number, name, address)

