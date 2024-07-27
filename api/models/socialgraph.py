"""
This module provides classes for representing the social in the Neo4j database using neomodel.

Entities:
    - `Person`: represents a person in the DB (both dead and alive)
        - `User`: child of `Person`, represents an active user 
    - `Group`: represents a group (of users) in the DB
        - `Classroom`: child of `Group`, represents a classroom 
        - `School`: child of `Group`, represents a school 

Intra-Relationships:
    - `User -[FRIENDS_WITH]-> User`
    - `User -[FOLLOWS]-> User`
    - `User -[MEMBER_OF]-> Group`
    - `Group -[PARENT]-> Group`

Dependencies:
    `neomodel`: The module relies on the neomodel library for interacting with the Neo4j database.
"""

from neomodel import (
    StructuredNode, StructuredRel, RelationshipTo, RelationshipFrom, # Relationship,
    UniqueIdProperty, StringProperty, BooleanProperty, #IntegerProperty,
    DateProperty, DateTimeProperty, EmailProperty,
    OneOrMore
)
from .contentgraph import VisitRel, FlagRel

# from uuid import uuid4

######################################################################
# RELATIONSHIPS
class FriendRel(StructuredRel):
    """
    Represents the relationship between two users in the Neo4j database.

    Attributes:
        since (datetime): The date the relationship was created.
        accepted (boolean): Whether the relationship was accepted.
        blocked (boolean): Whether the relationship was blocked.
    """
    created = DateTimeProperty(default_now=True)
    accepted = BooleanProperty(default=False)
    blocked = BooleanProperty(default=False)


class MembershipRel(StructuredRel):
    """
    Represents the relationship between a user and a group in the Neo4j database.

    Attributes:
        role (str): The role of the user in the group.
    """
    created = DateTimeProperty(default_now=True)
    role = StringProperty(required=True, choices={
        "user" : "User",
        "student" : "Student",
        "teacher" : "Teacher",
        "admin" : "Admin"
    }, index=True)


######################################################################
# ENTITIES
class Language(StructuredNode):
    """
    Represents a language in the Neo4j database to which content and users are connected.

    Attributes:
        name (str): The name of the language.
    """
    uid = UniqueIdProperty()
    name = StringProperty(required=True, index=True)

    users = RelationshipFrom('User', 'HAS_LANGUAGE')
    groups = RelationshipFrom('Group', 'HAS_LANGUAGE')
    notes = RelationshipFrom('Note', 'HAS_LANGUAGE')
    modules = RelationshipFrom('Module', 'HAS_LANGUAGE')


class Person(StructuredNode):
    """
    Represents a person in the Neo4j database, both dead and alive.

    Attributes:
        firstName (str): The first name of the person.
        lastName (str): The last name of the person.
        bithDate (datetime): The date of birth of the person.
    """
    uid = UniqueIdProperty() # not to be confused with Neo4j's 'id' property (don't use this in queries!)
    firstName = StringProperty(required=True)
    lastName = StringProperty(required=True)
    birthDate = DateProperty()
    bio = StringProperty(max_length=500)

    languages = RelationshipTo('Language', 'HAS_LANGUAGE')
    # social intra-relations
    followers = RelationshipFrom("User", "FOLLOWS")
    # social-knowledge inter-relations
    studies = RelationshipTo('Concept', 'STUDIES')
    interests = RelationshipTo('Subject', 'INTERESTED_IN')

class Email(StructuredNode):
    email = EmailProperty()

class User(Person):
    """
    Represents an active user in the Neo4j database.

    Attributes:
        username (str): The full name of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
    """
    username = StringProperty(required=True, unique_index=True, max_length=24)
    email = StringProperty(required=True, unique_index=True)
    password = StringProperty(required=True)
    signUp = DateTimeProperty(required=True)
    signIn = DateTimeProperty(required=True)

    # social intra-relations
    friends = RelationshipTo("User", "FRIENDS_WITH", model=FriendRel)
    groups = RelationshipTo("Group", "MEMBER_OF", model=MembershipRel)
    following = RelationshipTo("User", "FOLLOWS")
    # content inter-relations
    visited_modules = RelationshipTo('Module', 'VISITED', model=VisitRel)
    flagged_modules = RelationshipTo('Module', 'FLAGGED', model=FlagRel)
    notes = RelationshipTo('Note', 'CREATES')
    messages = RelationshipFrom('Note', 'SEND_TO')
    votes = RelationshipTo('Note', 'VOTES_ON')


class Group(StructuredNode):
    """
    Represents a group (of users) in the Neo4j database.

    Attributes:
        name (str): The name of the group.
        created (datetime): The date the group was created.
        bio (str): A brief description of the group.
    """
    uid = UniqueIdProperty()
    name = EmailProperty(required=True, index=True)
    created = DateTimeProperty(required=True)
    bio = StringProperty(max_length=500)

    languages = RelationshipTo('Language', 'HAS_LANGUAGE')
    # social intra-relations
    members = RelationshipFrom('User', 'MEMBER_OF', model=MembershipRel, cardinality=OneOrMore)
    # content inter-relations
    messages = RelationshipFrom('Note', 'SEND_TO')

class Classroom(Group):
    """
    Represents a classroom in the Neo4j database.
    """
    # social intra-relations
    modules = RelationshipTo('Module', 'CREATES')
    # social inter-relations
    groups = RelationshipFrom("Group", "PARENT", cardinality=OneOrMore)

class School(Classroom):
    """
    Represents a school in the Neo4j database.
    """
    # social intra-relations
    classes = RelationshipFrom("Classroom", "PARENT", cardinality=OneOrMore)