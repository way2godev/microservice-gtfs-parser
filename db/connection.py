import psycopg2

class PostgresConnection:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Connected to PostgreSQL database!")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL database:", error)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from PostgreSQL database.")

    def get_cursor(self):
        return self.connection.cursor()