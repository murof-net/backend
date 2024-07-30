from neomodel import (
    StructuredNode, RelationshipTo, RelationshipFrom,
    UniqueIdProperty, StringProperty, DateProperty, DateTimeProperty,
    OneOrMore
)

######################################################################

class Module(StructuredNode):
    name = StringProperty(required=True)
    content = StringProperty(required=True)
