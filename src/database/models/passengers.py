from peewee import CharField, IntegerField
from datetime import datetime

from src.database.connection import PostgresqlModel
from src.database.models.fields import DateTimeField

class PassengersModel(PostgresqlModel):
    """
    PassengersModel represents the database model for passengers in the system.
    Attributes:
        name (CharField): The name of the passenger. This is a required field with a maximum length of 255 characters.
        age (IntegerField): The age of the passenger. This is a required field.
        email (CharField): The email address of the passenger. This is a required field with a maximum length of 255 characters.
        created_at (DateTimeField): The timestamp indicating when the passenger record was created. 
            Defaults to the current date and time in ISO 8601 format with minute precision.
        updated_at (DateTimeField): The timestamp indicating when the passenger record was last updated. 
            Defaults to the current date and time in ISO 8601 format with minute precision.
    Meta:
        table_name (str): Specifies the name of the database table as 'passengers'.
    """
    name = CharField(max_length=255, null=False)
    age = IntegerField(null=False)
    email = CharField(max_length=255, null=False, unique=True)
    password = CharField(max_length=36, null=False)
    created_at = DateTimeField(
        default=datetime.now().isoformat(timespec="minutes"),formats=["%Y-%m-%dT%H:%M"])
    updated_at = DateTimeField(
        default=datetime.now().isoformat(timespec="minutes"),formats=["%Y-%m-%dT%H:%M"])
    
    class Meta:
        table_name = 'passengers'
