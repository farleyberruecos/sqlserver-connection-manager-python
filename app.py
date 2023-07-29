from connection.sqlserver_connection_manager_python import *

config = DatabaseConfig("database.ini")

# Agregar una nueva base de datos a la configuración
config.add_database("name block", "server", "database", "user", "pass")
connection_string = config.get_connection_string("name block")
query = "SELECT * FROM TableName"
connection.connect()
result = connection.execute_query(query)
for row in result:
    print(row)

    # Cerrar la conexión
connection.close()