from unit.models import Relationship


def create_relationship(type: str, id: str, relation: str = None):
    relation = relation or type
    return {relation: Relationship(type, id)}


def create_deposit_account_relationship(id: str, relation: str):
    return {relation: Relationship("depositAccount", id)}
