import pyodbc
from configparser import ConfigParser
import os


class DatabaseConfig:
    _instance = None

    def __new__(cls, filename):
        if not cls._instance:
            cls._instance = super(DatabaseConfig, cls).__new__(cls)
            cls._instance.filename = os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
            cls._instance.config = ConfigParser()
            cls._instance.config.read(cls._instance.filename)
        return cls._instance

    def get_connection_string(self, section):
        if section in self.config:
            config_section = self.config[section]
            server = config_section.get('server')
            database = config_section.get('database')
            username = config_section.get('username')
            password = config_section.get('password')
            return f"Driver={{SQL Server}};Server={server};Database={database};UID={username};PWD={password}"
        else:
            raise ValueError(f"Section '{section}' not found in the configuration file.")

    def add_database(self, section, server, database, username, password):
        if section not in self.config:
            self.config.add_section(section)
        self.config.set(section, 'server', server)
        self.config.set(section, 'database', database)
        self.config.set(section, 'username', username)
        self.config.set(section, 'password', password)
        with open(self.filename, 'w') as config_file:
            self.config.write(config_file)

class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(self.connection_string)
            self.cursor = self.connection.cursor()
            print("Connected to the database!")
        except pyodbc.Error as e:
            print(f"Error connecting to the database: {e}")


    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            if self.cursor.description is not None:
                rows = self.cursor.fetchall()
                return rows
        except pyodbc.Error as e:
            print(f"Error executing query: {e}")


    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed.")


if __name__ == "__main__":
    # Ejemplo de uso
    config = DatabaseConfig("database.ini")


    # Agregar una nueva base de datos a la configuración
    config.add_database("vmpdn", "vmpdn1", "analitica", "consultasbi", "juniortupapa")

    # Obtener la cadena de conexión para una base de datos específica
   # connection_string = config.get_connection_string("stopsserverdb")


    # Crear una instancia de DatabaseConnection y conectarse a la base de datos
    #connection = DatabaseConnection(connection_string)
    #connection.connect()


    # Ejecutar consultas en la base de datos
    #query = "SELECT * FROM [dbo].[modelthreshold79]"
    #result = connection.execute_query(query)
    #for row in result:
    #    print(row)
#

    # Cerrar la conexión
    #connection.close()
