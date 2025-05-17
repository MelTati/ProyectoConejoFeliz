from db.conexion import crear_conexion

class DetallesVentasModel:
    def __init__(self):
        self.conexion = crear_conexion()
    
    def obtener_detalles_venta(self, id_venta):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT dv.id_ventas, dv.codigo_articulo, a.nombre_articulo, 
                       a.precio_articulo, dv.cantidad, dv.subtotal
                FROM detalles_ventas dv
                JOIN articulos a ON dv.codigo_articulo = a.codigo_articulo
                WHERE dv.id_ventas = %s
                ORDER BY a.nombre_articulo
            """, (id_venta,))
            return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error al obtener detalles: {e}")
        finally:
            if self.conexion.is_connected():
                cursor.close()
    
    def agregar_articulo(self, id_venta, codigo_articulo, cantidad, subtotal):
        try:
            cursor = self.conexion.cursor()
            # Verificar si ya existe
            cursor.execute("""
                SELECT cantidad FROM detalles_ventas 
                WHERE id_ventas = %s AND codigo_articulo = %s
            """, (id_venta, codigo_articulo))
            existente = cursor.fetchone()
            
            if existente:
                nueva_cantidad = existente[0] + cantidad
                nuevo_subtotal = nueva_cantidad * (subtotal / cantidad)
                cursor.execute("""
                    UPDATE detalles_ventas
                    SET cantidad = %s, subtotal = %s
                    WHERE id_ventas = %s AND codigo_articulo = %s
                """, (nueva_cantidad, nuevo_subtotal, id_venta, codigo_articulo))
            else:
                cursor.execute("""
                    INSERT INTO detalles_ventas 
                    (id_ventas, codigo_articulo, cantidad, subtotal)
                    VALUES (%s, %s, %s, %s)
                """, (id_venta, codigo_articulo, cantidad, subtotal))
            
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Error al agregar artículo: {e}")
        finally:
            if self.conexion.is_connected():
                cursor.close()
    
    def eliminar_articulo(self, id_venta, codigo_articulo):
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                DELETE FROM detalles_ventas
                WHERE id_ventas = %s AND codigo_articulo = %s
            """, (id_venta, codigo_articulo))
            self.conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Error al eliminar artículo: {e}")
        finally:
            if self.conexion.is_connected():
                cursor.close()
    
    def obtener_total_venta(self, id_venta):
        try:
            cursor = self.conexion.cursor()
            cursor.execute("""
                SELECT SUM(subtotal) as total FROM detalles_ventas
                WHERE id_ventas = %s
            """, (id_venta,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado[0] else 0
        except Exception as e:
            raise Exception(f"Error al calcular total: {e}")
        finally:
            if self.conexion.is_connected():
                cursor.close()
    
    def obtener_ultima_venta(self):
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT id_ventas FROM ventas ORDER BY id_ventas DESC LIMIT 1")
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            raise Exception(f"Error al obtener última venta: {e}")
        finally:
            if self.conexion.is_connected():
                cursor.close()
    
    def buscar_articulo(self, busqueda):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT codigo_articulo, nombre_articulo, precio_articulo 
                FROM articulos 
                WHERE (codigo_articulo = %s OR nombre_articulo LIKE %s) 
                AND activacion_articulo = 1
                LIMIT 1
            """, (busqueda, f"%{busqueda}%"))
            return cursor.fetchone()
        except Exception as e:
            raise Exception(f"Error al buscar artículo: {e}")
        finally:
            if self.conexion.is_connected():
                cursor.close()
    
    def __del__(self):
        if hasattr(self, 'conexion') and self.conexion.is_connected():
            self.conexion.close()