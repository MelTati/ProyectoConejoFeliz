from db.conexion import crear_conexion

class LoginModel:
    def verificar_credenciales(self, usuario, contrasena):
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT * FROM usuarios u
                JOIN roles r ON u.id_roles = r.id_roles
                WHERE u.nombre_usuario = %s AND u.password = %s AND r.cargo IN ('Supervisor', 'Cajero')
            """, (usuario, contrasena))
            
            resultado = cursor.fetchone()
            cursor.close()
            conexion.close()
            
            return resultado
        except Exception as e:
            print(f"Error en LoginModel: {e}")
            raise