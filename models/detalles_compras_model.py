# models/detalles_compras_model.py
from db.conexion import crear_conexion

class DetallesComprasModel:
    def __init__(self):
        self.conexion = crear_conexion()
        self.cursor = self.conexion.cursor(dictionary=True)
        self.conexion.autocommit = True

    def obtener_detalles_compra(self, id_compras):
        try:
            self.cursor.execute("""
                SELECT dc.id_compras, dc.codigo_articulo, a.nombre_articulo,
                       a.costo_articulo, dc.cantidad, dc.subtotal,
                       m.nombre_marca, c.tipo_categoria
                FROM detalles_compras dc
                JOIN articulos a ON dc.codigo_articulo = a.codigo_articulo
                JOIN marcas m ON a.id_marca = m.id_marca
                JOIN categorias c ON a.id_categorias = c.id_categorias
                WHERE dc.id_compras = %s
                ORDER BY a.nombre_articulo
            """, (id_compras,))
            return self.cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error al obtener detalles: {e}")

    def obtener_total_compra(self, id_compras):
        try:
            self.cursor.execute("""
                SELECT SUM(subtotal) as total FROM detalles_compras
                WHERE id_compras = %s
            """, (id_compras,))
            resultado = self.cursor.fetchone()
            return resultado["total"] or 0
        except Exception as e:
            raise Exception(f"Error al calcular total: {e}")

    def agregar_articulo(self, id_compras, codigo_articulo, cantidad):
        try:
            # Obtener información del artículo
            self.cursor.execute("""
                SELECT costo_articulo FROM articulos 
                WHERE codigo_articulo = %s AND activacion_articulo = 1
            """, (codigo_articulo,))
            articulo = self.cursor.fetchone()
            
            if not articulo:
                raise Exception("Artículo no encontrado o no activo")

            # Verificar si ya existe en la compra
            self.cursor.execute("""
                SELECT cantidad FROM detalles_compras 
                WHERE id_compras = %s AND codigo_articulo = %s
            """, (id_compras, codigo_articulo))
            existente = self.cursor.fetchone()

            costo = articulo["costo_articulo"]
            
            if existente:
                nueva_cantidad = existente["cantidad"] + cantidad
                nuevo_subtotal = nueva_cantidad * costo
                
                self.cursor.execute("""
                    UPDATE detalles_compras
                    SET cantidad = %s, subtotal = %s
                    WHERE id_compras = %s AND codigo_articulo = %s
                """, (nueva_cantidad, nuevo_subtotal, id_compras, codigo_articulo))
            else:
                subtotal = cantidad * costo
                self.cursor.execute("""
                    INSERT INTO detalles_compras 
                    (id_compras, codigo_articulo, cantidad, subtotal)
                    VALUES (%s, %s, %s, %s)
                """, (id_compras, codigo_articulo, cantidad, subtotal))
            
            return True
        except Exception as e:
            raise Exception(f"Error al agregar artículo: {e}")

    def eliminar_articulo(self, id_compras, codigo_articulo):
        try:
            self.cursor.execute("""
                DELETE FROM detalles_compras
                WHERE id_compras = %s AND codigo_articulo = %s
            """, (id_compras, codigo_articulo))
            return self.cursor.rowcount > 0
        except Exception as e:
            raise Exception(f"Error al eliminar artículo: {e}")

    def buscar_articulo(self, busqueda):
        try:
            self.cursor.execute("""
                SELECT codigo_articulo, nombre_articulo, costo_articulo 
                FROM articulos 
                WHERE (codigo_articulo = %s OR nombre_articulo LIKE %s) 
                AND activacion_articulo = 1
                LIMIT 1
            """, (busqueda, f"%{busqueda}%"))
            return self.cursor.fetchone()
        except Exception as e:
            raise Exception(f"Error al buscar artículo: {e}")

    def obtener_ultima_compra(self):
        try:
            self.cursor.execute("""
                SELECT id_compras FROM compras 
                ORDER BY id_compras DESC LIMIT 1
            """)
            resultado = self.cursor.fetchone()
            return resultado["id_compras"] if resultado else None
        except Exception as e:
            raise Exception(f"Error al obtener última compra: {e}")

    def cerrar_conexion(self):
        self.cursor.close()
        self.conexion.close()