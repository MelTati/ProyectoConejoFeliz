from db.conexion import crear_conexion

class UsuariosModel:
    def __init__(self):
        self.conexion = crear_conexion()
        self.cursor = self.conexion.cursor(dictionary=True)
    
    def obtener_usuarios(self):
        try:
            self.cursor.execute("""
                SELECT u.id_usuario, u.nombre_usuario, u.telefono, u.password, r.cargo
                FROM usuarios u
                JOIN roles r ON u.id_roles = r.id_roles
            """)
            return self.cursor.fetchall()
        except Exception as e:
            raise e
    
    def obtener_roles(self):
        try:
            self.cursor.execute("SELECT id_roles, cargo FROM roles")
            return self.cursor.fetchall()
        except Exception as e:
            raise e
    
    def agregar_usuario(self, id_usuario, nombre, telefono, password, id_rol):
        try:
            self.cursor.execute("""
                INSERT INTO usuarios (id_usuario, nombre_usuario, telefono, password, id_roles)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_usuario, nombre, telefono, password, id_rol))
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            raise e
    
    def actualizar_usuario(self, nombre, telefono, password, id_rol, id_usuario):
        try:
            self.cursor.execute("""
                UPDATE usuarios
                SET nombre_usuario=%s, telefono=%s, password=%s, id_roles=%s
                WHERE id_usuario=%s
            """, (nombre, telefono, password, id_rol, id_usuario))
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            raise e
    
    def eliminar_usuario(self, id_usuario):
        try:
            self.cursor.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id_usuario,))
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            raise e
    
    def __del__(self):
        if self.conexion.is_connected():
            self.cursor.close()
            self.conexion.close()