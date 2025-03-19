from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from typing import List, Optional, Dict, Union
from src.schemas.types import EmailStr, AlphaStr, PasswordStr


class Login(BaseModel):
    """
    Login schema for user authentication.

    Attributes:
        email (str): Email address of a customer. Example: 'user@example.com'.
        password (str): Customer password.

    Methods:
        validate_email(cls, value): Validates the format of the email address.
            Args:
                value (str): The email address to validate.
            Returns:
                str: The validated email address.
            Raises:
                ValueError: If the email address format is invalid.
    """
    email: EmailStr = Field(..., example='user@example.com', description='Email address of a customer', examples="email@example.com")
    password: PasswordStr = Field(..., description='Customer password', examples="Password123!")


class ReservationRequestSchema(BaseModel):
    scheduled_at: str = Field(datetime.now().isoformat(timespec='minutes'), title="Date of reservation", description="The date of the reservation in the format YYYY-MM-DD")
    destination: str = Field(..., title="Destination", description="The destination of the reservation")


class PassengerIdRequestSchema(BaseModel):
    passenger_id: int = Field(..., title="Passenger ID", description="The ID of the passenger to associate with the reservation")


class PassengerRequestSchema(BaseModel):
    name: AlphaStr = Field(..., title="Name for the passenger", examples="Jonh")
    age: int = Field(..., title="Age for the passenger", examples=18)
    email: EmailStr = Field(..., title="Email for the passenger", examples="user@example.com")
    password: PasswordStr = Field(..., title="Password for the passenger", examples="Password123!")
