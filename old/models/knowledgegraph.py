"""
This module provides classes for representing the knowledge graph in the Neo4j database using neomodel.

Entities:
    - `Concept`: represents a concept in the DB (non-hierarchicaly structured)
    - `Subject`: represents a subject (hierarchicaly structured)

Intra-Relationships:
    - `Concept -[REFERENCES]-> Concept`
    - `Concept -[RELATES_TO]-> Subject`
    - `Subject -[PARENT]-> Subject`

Dependencies:
    `neomodel`: The module relies on the neomodel library for interacting with the Neo4j database.
"""

from neomodel import (
    StructuredNode, RelationshipTo, RelationshipFrom,
    UniqueIdProperty, StringProperty,
    OneOrMore
)

######################################################################
# NODES
class Concept(StructuredNode):
    """
    Represents a concept in the Neo4j database (non-hierarchically structured).

    Attributes:
        name (str): The name of the concept.
        description (str): A brief description of the concept in English.
    """
    uid = UniqueIdProperty()
    name = StringProperty(required=True, index=True)
    description = StringProperty()
    # TODO node embeddings?!

    # knowledge intra-relations
    references = RelationshipTo("Concept", "REFERENCES", cardinality=OneOrMore)
    subjects = RelationshipTo("Subject", "RELATES_TO", cardinality=OneOrMore)
    # social inter-relations
    users = RelationshipFrom("User", "STUDIES")
    # content inter-relations
    notes = RelationshipFrom("Note", "EXPLAINS")


class Subject(StructuredNode):
    """
    Represents a subject in the Neo4j database (hierarchically structured).

    Attributes:
        name (str): The name of the subject.
        description (str): A brief description of the subject in English.
    """
    uid = UniqueIdProperty()
    name = StringProperty(required=True, index=True)
    description = StringProperty()
    # TODO node embeddings?!?
    
    # knowledge intra-relations
    parent = RelationshipTo("Subject", "PARENT")
    child_subjects = RelationshipFrom("Subject", "PARENT")
    child_concepts = RelationshipFrom("Concept", "RELATES_TO")
    # social inter-relations
    users = RelationshipFrom("User", "INTERESTED_IN")
    groups = RelationshipFrom("Group", "STUDIES")
    # content inter-relations
    modules = RelationshipFrom("Module", "EXPLAINS")
