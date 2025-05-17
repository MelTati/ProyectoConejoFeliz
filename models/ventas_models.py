from db.conexion import crear_conexion

class VentasModel:
    def __init__(self):
        self.conexion = crear_conexion()
        self.cursor = self.conexion.cursor(dictionary=True)
    
    def obtener_usuarios(self):
        self.cursor.execute(""" 
            SELECT u.id_usuario, u.nombre_usuario, u.telefono, r.cargo
            FROM usuarios u
            JOIN roles r ON u.id_roles = r.id_roles
        """)
        return self.cursor.fetchall()
    
    def obtener_clientes(self):
        self.cursor.execute("SELECT id_cliente, nombre, telefono FROM cliente")
        return self.cursor.fetchall()
    
    def obtener_ventas(self):
        self.cursor.execute("""
            SELECT v.id_ventas, v.fecha_venta,
                   u.nombre_usuario, u.telefono AS telefono_usuario,
                   c.nombre AS nombre_cliente, c.telefono AS telefono_cliente,
                   dv.codigo_articulo, a.nombre_articulo, dv.cantidad, dv.subtotal
            FROM ventas v
            JOIN usuarios u ON v.id_usuario = u.id_usuario
            JOIN cliente c ON v.id_cliente = c.id_cliente
            LEFT JOIN detalles_ventas dv ON v.id_ventas = dv.id_ventas
            LEFT JOIN articulos a ON dv.codigo_articulo = a.codigo_articulo
            GROUP BY v.id_ventas, dv.codigo_articulo
        """)
        return self.cursor.fetchall()
    
    def agregar_venta(self, fecha_venta, id_usuario, id_cliente):
        self.cursor.execute("""
            INSERT INTO ventas (fecha_venta, id_usuario, id_cliente)
            VALUES (%s, %s, %s)
        """, (fecha_venta, id_usuario, id_cliente))
        self.conexion.commit()
        return self.cursor.lastrowid
    
    def actualizar_venta(self, fecha_venta, id_usuario, id_cliente, id_ventas):
        self.cursor.execute("""
            UPDATE ventas
            SET fecha_venta=%s, id_usuario=%s, id_cliente=%s
            WHERE id_ventas=%s
        """, (fecha_venta, id_usuario, id_cliente, id_ventas))
        self.conexion.commit()
    
    def eliminar_venta(self, id_ventas):
        self.cursor.execute("DELETE FROM detalles_ventas WHERE id_ventas = %s", (id_ventas,))
        self.cursor.execute("DELETE FROM ventas WHERE id_ventas = %s", (id_ventas,))
        self.conexion.commit()
    
    def obtener_detalles_venta(self, id_ventas):
        self.cursor.execute("""
            SELECT v.id_ventas, v.fecha_venta,
                   u.nombre_usuario, u.telefono AS telefono_usuario,
                   c.nombre AS nombre_cliente, c.telefono AS telefono_cliente,
                   dv.codigo_articulo, a.nombre_articulo, dv.cantidad, dv.subtotal
            FROM ventas v
            JOIN usuarios u ON v.id_usuario = u.id_usuario
            JOIN cliente c ON v.id_cliente = c.id_cliente
            LEFT JOIN detalles_ventas dv ON v.id_ventas = dv.id_ventas
            LEFT JOIN articulos a ON dv.codigo_articulo = a.codigo_articulo
            WHERE v.id_ventas = %s
            LIMIT 1
        """, (id_ventas,))
        return self.cursor.fetchone()
    
    def obtener_totales_venta(self, id_ventas):
        self.cursor.execute("""
            SELECT COUNT(*) as total_articulos, SUM(subtotal) as total_venta
            FROM detalles_ventas
            WHERE id_ventas = %s
        """, (id_ventas,))
        return self.cursor.fetchone()
    
    def __del__(self):
        self.cursor.close()
        self.conexion.close()