import re

def validate_only_letters(value: str):
    """
    Validate that the input string contains only letters.

    Args:
        value (str): The string to be validated.

    Returns:
        str: The validated string if it contains only letters.

    Raises:
        ValueError: If the string contains non-letter characters.
    """
    if not value.isalpha():
        raise ValueError('Only letters are allowed')
    return value


def validate_email(value: str):
    """
    Validates the email field after it has been set.

    This method uses a regular expression to check if the provided email
    address matches the standard email format. If the email does not match
    the expected format, a ValueError is raised.

    Args:
        cls: The class the method is attached to.
        value (str): The email address to validate.

    Returns:
        str: The validated email address.

    Raises:
        ValueError: If the email address does not match the expected format.
    """
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
        raise ValueError('Invalid email format, it should be like: test@example.com')
    return value


def validate_phone_number(value: str):
    """
    Validates a phone number to ensure it meets specific criteria.

    Args:
        value (str): The phone number to validate.

    Returns:
        str: The validated phone number.

    Raises:
        ValueError: If the phone number is not between 10 and 15 digits long,
                    or if it does not start with a '+' character.
    """
    if len(value) < 10 or len(value) > 15:
        raise ValueError('Phone number should be 10-15 digits long')
    elif not str(value).startswith('+'):
        raise ValueError('Phone number should start with +')
    return value


def validate_password(value: str):
    """
    Validates a password to ensure it meets specific criteria.

    Args:
        value (str): The password to validate.

    Returns:
        str: The validated password.

    Raises:
        ValueError: If the password is not at least 8 characters long,
                    or if it does not contain at least one uppercase letter,
                    one lowercase letter, and one digit.
    """
    if len(value) < 8:
        raise ValueError('Password should be at least 8 characters long')
    elif not any(char.isupper() for char in value):
        raise ValueError('Password should contain at least one uppercase letter')
    elif not any(char.islower() for char in value):
        raise ValueError('Password should contain at least one lowercase letter')
    elif not any(char.isdigit() for char in value):
        raise ValueError('Password should contain at least one digit')
    return value
