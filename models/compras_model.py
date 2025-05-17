from db.conexion import crear_conexion

class ComprasModel:
    def __init__(self):
        self.conexion = crear_conexion()

    def crear_compra(self, id_compras, rfc, fecha_compras):
        with self.conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO compras (id_compras, RFC, fecha_compras) VALUES (%s, %s, %s)",
                (id_compras, rfc, fecha_compras)
            )
            self.conexion.commit()

    def obtener_compras(self):
        with self.conexion.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT c.id_compras, p.nombre_proveedor, c.fecha_compras,
                       IFNULL(SUM(dc.subtotal), 0) AS total
                FROM compras c
                JOIN proveedor p ON c.RFC = p.RFC 
                LEFT JOIN detalles_compras dc ON c.id_compras = dc.id_compras
                GROUP BY c.id_compras
                ORDER BY c.id_compras DESC
            """)
            return cursor.fetchall()

    def eliminar_compra(self, id_compras):
        with self.conexion.cursor() as cursor:
            cursor.execute("DELETE FROM compras WHERE id_compras = %s", (id_compras,))
            self.conexion.commit()

    def obtener_proveedores(self):
        with self.conexion.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT RFC, nombre_proveedor FROM proveedor")
            return cursor.fetchall()