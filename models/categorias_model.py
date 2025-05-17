from db.conexion import crear_conexion

class CategoriaModel:
    @staticmethod
    def obtener_todas():
        conexion = crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM categorias")
            return cursor.fetchall()
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def agregar(tipo_categoria):
        conexion = crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO categorias (tipo_categoria) VALUES (%s)",
                (tipo_categoria,)
            )
            conexion.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar(id_categoria, tipo_categoria):
        conexion = crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "UPDATE categorias SET tipo_categoria=%s WHERE id_categorias=%s",
                (tipo_categoria, id_categoria))
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar(id_categoria):
        conexion = crear_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM categorias WHERE id_categorias=%s", (id_categoria,))
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conexion.close()