from db.conexion import crear_conexion

class MarcasModel:
    def __init__(self):
        self.conexion = crear_conexion()
        self.cursor = self.conexion.cursor(dictionary=True)

    def obtener_marcas(self):
        try:
            self.cursor.execute("""
                SELECT marcas.id_marca, marcas.nombre_marca, proveedor.nombre_proveedor
                FROM marcas
                JOIN proveedor ON marcas.RFC = proveedor.RFC
            """)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener marcas: {e}")
            return []

    def obtener_proveedores(self):
        try:
            self.cursor.execute("SELECT RFC, nombre_proveedor FROM proveedor")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener proveedores: {e}")
            return []

    def agregar_marca(self, nombre, rfc):
        try:
            self.cursor.execute("INSERT INTO marcas (nombre_marca, RFC) VALUES (%s, %s)", (nombre, rfc))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al agregar marca: {e}")
            return False

    def actualizar_marca(self, id_marca, nombre, rfc):
        try:
            self.cursor.execute(
                "UPDATE marcas SET nombre_marca=%s, RFC=%s WHERE id_marca=%s",
                (nombre, rfc, id_marca))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar marca: {e}")
            return False

    def eliminar_marca(self, id_marca):
        try:
            self.cursor.execute("DELETE FROM marcas WHERE id_marca=%s", (id_marca,))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar marca: {e}")
            return False

    def __del__(self):
        if self.conexion.is_connected():
            self.cursor.close()
            self.conexion.close()