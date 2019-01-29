from uuid import uuid4, UUID


def get_uuid():
    """Returns a unique UUID string that will be used as a minion id.
    Generates a UUID string and verifies it is unique.
    Continue generating UUIDs until a unique one is generated.
    """
    return str(uuid4())


def validate_uuid(uuid_string):
    """Validates a given string as a valid UUID
    Args:
        uuid_string: The string to validate
    Returns:
        True if a valid UUID, else false
    """
    try:
        UUID(uuid_string, version=4)
        return True
    except:
        return False
