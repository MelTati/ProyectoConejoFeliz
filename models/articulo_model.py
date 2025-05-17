import mysql.connector
from db.conexion import crear_conexion
    
class ArticuloModel:
    @staticmethod
    def obtener_articulos(filtros):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor(dictionary=True)
            query = """
                SELECT a.codigo_articulo, a.nombre_articulo, a.activacion_articulo,
                    a.precio_articulo, a.costo_articulo,
                    c.tipo_categoria, m.nombre_marca, a.descr_caracteristicas,
                    a.cantidad_maxima, a.cantidad_minima,
                    COALESCE(a.stock, 0) + COALESCE(SUM(dc.cantidad), 0) - COALESCE(SUM(dv.cantidad), 0) AS stock
                FROM articulos a
                JOIN categorias c ON a.id_categorias = c.id_categorias
                JOIN marcas m ON a.id_marca = m.id_marca
                LEFT JOIN detalles_compras dc ON a.codigo_articulo = dc.codigo_articulo
                LEFT JOIN detalles_ventas dv ON a.codigo_articulo = dv.codigo_articulo
                WHERE (%s IS NULL OR a.id_categorias = %s)
                AND (%s IS NULL OR a.id_marca = %s)
                AND (a.codigo_articulo LIKE %s OR a.nombre_articulo LIKE %s)
                GROUP BY a.codigo_articulo, a.nombre_articulo, a.activacion_articulo, 
                        a.precio_articulo, a.costo_articulo, c.tipo_categoria, 
                        m.nombre_marca, a.descr_caracteristicas, a.cantidad_maxima, 
                        a.cantidad_minima
            """
            cursor.execute(query, filtros)
            resultados = cursor.fetchall()
            return resultados
        except mysql.connector.Error as err:
            print(f"Error al obtener artículos: {err}")
            raise
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexion' in locals() and conexion:
                conexion.close()

    @staticmethod
    def obtener_categorias():
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id_categorias, tipo_categoria FROM categorias")
            resultados = cursor.fetchall()
            return resultados
        except mysql.connector.Error as err:
            print(f"Error al obtener categorías: {err}")
            raise
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexion' in locals() and conexion:
                conexion.close()

    @staticmethod
    def obtener_marcas():
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id_marca, nombre_marca FROM marcas")
            resultados = cursor.fetchall()
            return resultados
        except mysql.connector.Error as err:
            print(f"Error al obtener marcas: {err}")
            raise
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexion' in locals() and conexion:
                conexion.close()

    @staticmethod
    def crear_articulo(datos):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO articulos (codigo_articulo, nombre_articulo, activacion_articulo,
                                       precio_articulo, costo_articulo, id_categorias, id_marca, descr_caracteristicas,
                                       cantidad_maxima, cantidad_minima, stock)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, datos)
            conexion.commit()
        except mysql.connector.Error as err:
            print(f"Error al crear artículo: {err}")
            raise
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexion' in locals() and conexion:
                conexion.close()

    @staticmethod
    def actualizar_articulo(datos):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE articulos
                SET nombre_articulo = %s, activacion_articulo = %s, precio_articulo = %s,
                    costo_articulo = %s, id_categorias = %s, id_marca = %s, descr_caracteristicas = %s, 
                    cantidad_maxima = %s, cantidad_minima =%s, stock = %s
                WHERE codigo_articulo = %s
            """, datos)
            conexion.commit()
        except mysql.connector.Error as err:
            print(f"Error al actualizar artículo: {err}")
            raise
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexion' in locals() and conexion:
                conexion.close()
    
    @staticmethod
    def eliminar_articulo(codigo):
        if not codigo:
            raise ValueError("El código del artículo no puede estar vacío")
        
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            
            # Verificar si el artículo existe primero
            cursor.execute("SELECT 1 FROM articulos WHERE codigo_articulo = %s", (codigo,))
            if not cursor.fetchone():
                raise ValueError("El artículo no existe")
            
            # Verificar si hay registros relacionados
            cursor.execute("""
                SELECT 1 FROM detalles_compras 
                WHERE codigo_articulo = %s 
                UNION ALL
                SELECT 1 FROM detalles_ventas 
                WHERE codigo_articulo = %s 
                LIMIT 1
            """, (codigo, codigo))
            
            if cursor.fetchone():
                raise ValueError("No se puede eliminar: el artículo tiene movimientos registrados")
            
            cursor.execute("DELETE FROM articulos WHERE codigo_articulo = %s", (codigo,))
            conexion.commit()
            
        except mysql.connector.Error as err:
            raise Exception(f"Error de base de datos: {err}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexion' in locals() and conexion:
                conexion.close()