import uuid

from unit.models import Relationship


def create_relationship(_type: str, _id: str, relation: str = None):
    relation = relation or _type
    return {relation: Relationship(_type, _id)}


def generate_uuid():
    return str(uuid.uuid1())

