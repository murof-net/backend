from neomodel import (
    AsyncStructuredNode, 
    # AsyncRelationshipTo, 
    # AsyncRelationshipFrom, 
    UniqueIdProperty,
    StringProperty, 
    EmailProperty,
    # RegexProperty, 
    # DateProperty, 
    DateTimeProperty, 
    BooleanProperty,
    # ArrayProperty
)

class User(AsyncStructuredNode):
    uid = UniqueIdProperty()
    is_verified = BooleanProperty(default=False)
    created_at = DateTimeProperty(default_now=True)
    last_login = DateTimeProperty(default_now=True)

    username = StringProperty(unique_index=True, required=True, min_length=3, max_length=32)
    email = EmailProperty(unique_index=True, required=True)
    hashed_password = StringProperty(required=True, min_length=8, max_length=64)
    # birthdate = DateProperty(required=True)
    # bio = StringProperty(max_length=256, default="")