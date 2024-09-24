from neomodel import (
    AsyncStructuredNode, 
    AsyncRelationshipTo, 
    AsyncRelationshipFrom, 
    StringProperty, 
    RegexProperty, 
    DateProperty, 
    DateTimeProperty, 
    BooleanProperty
)

class User(AsyncStructuredNode):
    username = StringProperty(unique_index=True, required=True)
    email = RegexProperty(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        required=True, unique_index=True)
    hashed_password = StringProperty(required=True)