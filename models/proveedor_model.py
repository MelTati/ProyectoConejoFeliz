from db.conexion import crear_conexion

class ProveedorModel:
    def __init__(self):
        self.conexion = crear_conexion()
        self.cursor = self.conexion.cursor(dictionary=True)

    def obtener_proveedores(self):
        try:
            self.cursor.execute("SELECT * FROM proveedor")
            return self.cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error al obtener proveedores: {e}")

    def agregar_proveedor(self, rfc, nombre, direccion, telefono, email):
        try:
            self.cursor.execute(
                "INSERT INTO proveedor (RFC, nombre_proveedor, direccion, telefono, email) VALUES (%s, %s, %s, %s, %s)",
                (rfc, nombre, direccion, telefono, email)
            )
            self.conexion.commit()
            return True
        except Exception as e:
            raise Exception(f"Error al agregar proveedor: {e}")

    def actualizar_proveedor(self, rfc, nombre, direccion, telefono, email):
        try:
            self.cursor.execute(
                "UPDATE proveedor SET nombre_proveedor=%s, direccion=%s, telefono=%s, email=%s WHERE RFC=%s",
                (nombre, direccion, telefono, email, rfc)
            )
            self.conexion.commit()
            return True
        except Exception as e:
            raise Exception(f"Error al actualizar proveedor: {e}")

    def eliminar_proveedor(self, rfc):
        try:
            self.cursor.execute("DELETE FROM proveedor WHERE RFC=%s", (rfc,))
            self.conexion.commit()
            return True
        except Exception as e:
            raise Exception(f"Error al eliminar proveedor: {e}")

    def __del__(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conexion') and self.conexion.is_connected():
            self.conexion.close()