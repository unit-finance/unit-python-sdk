from typing import Dict

from unit.models import Relationship, RelationshipArray


def create_relationship(type: str, id: str, relation: str = None):
    relation = relation or type
    return {relation: Relationship(type, id)}


def create_deposit_account_relationship(id: str, relation: str):
    return {relation: Relationship("depositAccount", id)}


def to_relationships(data: Dict):
    if data is None:
        return None

    relationships = dict()
    for k, v in data.items():
        if isinstance(v["data"], list):
            relationships[k] = RelationshipArray(v["data"])
        else:
            relationships[k] = Relationship(v["data"]["type"], v["data"]["id"])

    return relationships
