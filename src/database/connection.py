from peewee import PostgresqlDatabase, Model

from src.utils.config import Config

settings = Config()

class DatabaseConnection:
    """
    Singleton class to manage the database connection.
    This class ensures that only one instance of the database connection exists
    throughout the application. It uses the PostgreSQL database and retrieves
    connection settings from a settings module.
    Methods
    -------
    connect():
        Opens the database connection if it is closed.
    close():
        Closes the database connection if it is open.
    get_db():
        Returns the database instance.
    """
    _instance = None 

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize_connection()
        return cls._instance

    def _initialize_connection(self):
        self.db = PostgresqlDatabase(
            **{
                'database': settings.database_name,
                'user': settings.database_user,
                'password': settings.database_password,
                'host': settings.database_host,
                'port': settings.database_port
            }
        )

    def connect(self):
        if self.db.is_closed():
            self.db.connect()

    def close(self):
        if not self.db.is_closed():
            self.db.close()

    def get_db(self):
        return self.db

database = DatabaseConnection().get_db()

class PostgresqlModel(Model):
    class Meta:
        database = database
        schema = 'public'
