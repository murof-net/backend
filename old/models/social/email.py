from neomodel import StructuredNode, EmailProperty

class Email(StructuredNode):
    """
    Email node in the Neo4j database.
    Properties:
        email (str): The email address of the user. Used as the primary key.
    """
    email = EmailProperty(required=True, unique_index=True)