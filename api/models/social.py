from neomodel import (
    AsyncStructuredNode, 
    AsyncRelationshipTo, 
    AsyncRelationshipFrom, 
    UniqueIdProperty,
    StringProperty, 
    EmailProperty,
    # RegexProperty, 
    DateProperty, 
    DateTimeProperty, 
    BooleanProperty,
    # ArrayProperty
)

class User(AsyncStructuredNode):
    uid = UniqueIdProperty()
    verified = BooleanProperty(default=False)
    created_at = DateTimeProperty(default_now=True)

    # first_name = StringProperty(required=True, min_length=1, max_length=32)
    # last_name = StringProperty(required=True, min_length=1, max_length=32)
    username = StringProperty(unique_index=True, required=True, min_length=3, max_length=32)
    email = EmailProperty(unique_index=True, required=True)
    hashed_password = StringProperty(required=True, min_length=8, max_length=64)
    # birthdate = DateProperty(required=True)
    # bio = StringProperty(max_length=256, default="")

    # def full_name(self):
    #     return f"{self.first_name} {self.last_name}"