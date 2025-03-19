from peewee import CharField, ForeignKeyField
from datetime import datetime

from src.database.connection import PostgresqlModel
from src.database.models.fields import DateTimeField
from src.database.models.passengers import PassengersModel

class ReservationsModel(PostgresqlModel):
    """
    ReservationsModel represents a database model for storing reservation details.

    Attributes:
        destination (CharField): The destination of the reservation. This field is required and has a maximum length of 255 characters.
        scheduled_at (DateTimeField): The scheduled date and time for the reservation. This field is required and follows the format "%Y-%m-%dT%H:%M".
        created_at (DateTimeField): The timestamp when the reservation was created. Defaults to the current date and time in the format "%Y-%m-%dT%H:%M".
        updated_at (DateTimeField): The timestamp when the reservation was last updated. Defaults to the current date and time in the format "%Y-%m-%dT%H:%M".
        passenger_id (ForeignKeyField): A foreign key reference to the PassengersModel. This establishes a relationship with the passenger who made the reservation. Updates and deletions cascade.

    Meta:
        table_name (str): The name of the database table associated with this model ('reservations').
    """
    destination = CharField(max_length=255, null=False)
    scheduled_at = DateTimeField(null=False, formats=["%Y-%m-%dT%H:%M"])
    created_at = DateTimeField(default=datetime.now().isoformat(timespec="minutes"),formats=["%Y-%m-%dT%H:%M"])
    updated_at = DateTimeField(default=datetime.now().isoformat(timespec="minutes"),formats=["%Y-%m-%dT%H:%M"])
    passenger_id = ForeignKeyField(PassengersModel, backref='reservations', on_update='CASCADE', on_delete='CASCADE', null=True, default=None)
    class Meta:
        table_name = 'reservations'
