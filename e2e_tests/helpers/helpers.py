from unit.models import Relationship

def create_relationship(type: str, id: str, relation: str = None):
    relation = relation or type
    return {relation: Relationship(type, id)}
