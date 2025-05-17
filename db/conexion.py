import mysql.connector

def crear_conexion():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql",
            database="mydb_conejo_feliz"
        )
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        raise