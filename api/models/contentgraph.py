"""
This module provides classes for representing the content network in the Neo4j database using neomodel.

Entities:
    - `Note`: represents a note in the DB
        - `Message`: child of Note, represents a message
    - `Module`: represents a module in the DB
        - `LearningModule`: child of Module, represents a learning module

Intra-Relationships:
    - `Note -[COMMENTS_ON]-> Note`
    - `Note -[CONTENT_OF]-> Module`
    - `Module -[PARENT]-> Module`

Dependencies:
    `neomodel`: The module relies on the neomodel library for interacting with the Neo4j database.
"""

from neomodel import (
    StructuredNode, StructuredRel, RelationshipTo, RelationshipFrom,
    UniqueIdProperty, StringProperty, BooleanProperty, IntegerProperty,
    DateProperty, DateTimeProperty, #EmailProperty,
    OneOrMore
)

######################################################################
# RELATIONSHIPS
class VisitRel(StructuredRel):
    """
    Represents the relationship between a user and a module in the Neo4j database.

    Attributes:
        created (datetime): The date the relationship was created.
        last_visit (datetime): The last time the user visited the module.
    """
    created = DateProperty(default_now=True)
    lastVisit = DateTimeProperty(default_now=True, index=True)

class FlagRel(StructuredRel):
    """
    Represents the relationship between a user and a module in the Neo4j database.

    Attributes:
        created (datetime): The date the relationship was created.
    """
    created = DateTimeProperty(default_now=True, index=True)

class VoteRel(StructuredRel):
    """
    Represents the relationship between a user and a piece of content in the Neo4j database.

    Attributes:
        created (datetime): The date the relationship was created.
        vote (boolean): The vote of the user on the content.
    """
    created = DateProperty(default_now=True)
    vote = BooleanProperty()

class ContentRel(StructuredRel):
    """
    Represents the relationship between a module and a piece of content in the Neo4j database.

    Attributes:
        index (integer): The index of the content in the module.
    """
    index = IntegerProperty()


######################################################################
# ENTITIES
class Note(StructuredNode):
    """
    Represents a content note in the Neo4j database (markdown).

    Attributes:
        content (str): The content of the note.
        created (datetime): The date the note was created.
        modified (datetime): The date the note was last modified.
    """
    uid = UniqueIdProperty()
    content = StringProperty(required=True)
    created = DateTimeProperty(default_now=True)
    modified = DateTimeProperty(default_now=True)

    language = RelationshipTo("Language", "HAS_LANGUAGE", cardinality=OneOrMore)
    # content intra-relations
    content_of = RelationshipTo("Module", "CONTENT_OF", model=ContentRel)
    comments = RelationshipFrom("Note", "COMMENTS_ON")
    target = RelationshipTo("Note", "COMMENTS_ON")
    # social inter-relations
    created_by = RelationshipFrom("User", "CREATES", cardinality=OneOrMore)
    votes = RelationshipTo("User", "VOTES_ON", model=VoteRel)
    # knowledge inter-relations
    concepts = RelationshipTo("Concept", "EXPLAINS")

class Message(Note):
    """
    Represents a message in the Neo4j database.
    """
    recipient_users = RelationshipTo("User", "SEND_TO")
    recipient_groups = RelationshipTo("Group", "SEND_TO")

class Module(StructuredNode):
    """
    Represents a module in the Neo4j database.

    Attributes:
        name (str): The name of the module.
        created (datetime): The date the module was created.
        description (str): A brief description of the module.
    """
    uid = UniqueIdProperty()
    name = StringProperty(required=True, index=True)
    created = DateTimeProperty(default_now=True)
    modified = DateTimeProperty(default_now=True)

    language = RelationshipTo("Language", "HAS_LANGUAGE", cardinality=OneOrMore)
    # content intra-relations
    parents = RelationshipTo("Module", "PARENT")
    contents = RelationshipFrom("Note", "CONTENT_OF", model=ContentRel, cardinality=OneOrMore)
    # social inter-relations
    visits = RelationshipFrom("User", "VISITED", model=VisitRel)
    flags = RelationshipFrom("User", "FLAGGED", model=FlagRel)
    classes = RelationshipFrom("Classroom", "CREATES", cardinality=OneOrMore)
    # knowledge inter-relations
    subjects = RelationshipTo("Subject", "EXPLAINS")

# class LearningModule(Module):
#     """
#     Represents a learning module in the Neo4j database.

#     Attributes:
#     """
#     pass
#     # TODO: Extend modules into Learning/Testing modules?