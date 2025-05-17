from db.conexion import crear_conexion

class ClienteModel:
    def __init__(self):
        self.conexion = crear_conexion()
        self.cursor = self.conexion.cursor(dictionary=True)

    def obtener_clientes(self):
        try:
            self.cursor.execute("SELECT * FROM cliente")
            return self.cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error al obtener clientes: {e}")

    def agregar_cliente(self, nombre, telefono):
        try:
            self.cursor.execute(
                "INSERT INTO cliente (nombre, telefono) VALUES (%s, %s)",
                (nombre, telefono)
            )
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Error al agregar cliente: {e}")

    def actualizar_cliente(self, id_cliente, nombre, telefono):
        try:
            self.cursor.execute(
                "UPDATE cliente SET nombre=%s, telefono=%s WHERE id_cliente=%s",
                (nombre, telefono, id_cliente)
            )
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Error al actualizar cliente: {e}")

    def eliminar_cliente(self, id_cliente):
        try:
            self.cursor.execute(
                "DELETE FROM cliente WHERE id_cliente=%s",
                (id_cliente,)
            )
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Error al eliminar cliente: {e}")

    def __del__(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conexion') and self.conexion.is_connected():
            self.conexion.close()