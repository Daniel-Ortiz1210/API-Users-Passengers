from pydantic import AfterValidator
from typing import Annotated

from src.schemas.validators import validate_only_letters, validate_email, validate_phone_number

AlphaStr = Annotated[str, AfterValidator(validate_only_letters)]

EmailStr = Annotated[str, AfterValidator(validate_email)]

PhoneNumberStr = Annotated[str, AfterValidator(validate_phone_number)]
