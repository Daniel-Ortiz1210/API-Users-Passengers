from peewee import DateTimeField

class DateTimeField(DateTimeField):
    """
    A custom DateTimeField class that inherits from the base DateTimeField.
    Methods:
        db_value(value):
            Converts the given value to a database-compatible format using the parent class's db_value method.
        python_value(value):
            Converts the given value to a string formatted as "%Y-%m-%dT%H:%M".
    """

    def db_value(self, value):
        return super().db_value(value)
    
    def python_value(self, value):
        return value.strftime("%Y-%m-%dT%H:%M")
    