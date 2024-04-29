import psycopg2
import os

class PostgresConnection:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self, logger=None):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if logger:
                logger.info("Connected to PostgreSQL database.")
        except (Exception, psycopg2.Error) as error:
            if logger:
                logger.error("Error while connecting to PostgreSQL database:", error)
                os._exit(1)
            else:
                print("Error while connecting to PostgreSQL database:", error)
                os._exit(1)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from PostgreSQL database.")

    def get_cursor(self):
        return self.connection.cursor()
    
class Connection:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = PostgresConnection(*args, **kwargs)
        return cls._instance
    
    @staticmethod  
    def get_cursor():
        return Connection().get_cursor()