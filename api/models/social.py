from neomodel import StructuredNode, RelationshipTo, RelationshipFrom, StringProperty, RegexProperty, DateProperty, DateTimeProperty, BooleanProperty


class Language(StructuredNode):
    name = StringProperty(
        unique_index=True, required=True, 
        choices={
            "English": "en",
            "Dutch": "nl",
            "French": "fr",
            "German": "de",
            "Spanish": "es",
            "Korean": "ko"
            })
    users = RelationshipFrom('User', 'HAS_LANGUAGE')


class User(StructuredNode):
    first_name = StringProperty(required=True, max_length=30)
    last_name = StringProperty(required=True, max_length=30)
    email = RegexProperty(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        required=True, unique_index=True)
    hashed_password = StringProperty(required=True)
    birth_date = DateProperty(required=True)
    registration = DateTimeProperty(default_now=True)
    disabled = BooleanProperty(default=False)

    languages = RelationshipTo('Language', 'HAS_LANGUAGE')