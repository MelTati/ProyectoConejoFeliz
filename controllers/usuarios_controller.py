from models.usuarios_model import UsuariosModel

class UsuariosController:
    def __init__(self):
        self.model = UsuariosModel()
    
    def obtener_usuarios(self):
        return self.model.obtener_usuarios()
    
    def obtener_roles(self):
        return self.model.obtener_roles()
    
    def agregar_usuario(self, id_usuario, nombre, telefono, password, id_rol):
        return self.model.agregar_usuario(id_usuario, nombre, telefono, password, id_rol)
    
    def actualizar_usuario(self, nombre, telefono, password, id_rol, id_usuario):
        return self.model.actualizar_usuario(nombre, telefono, password, id_rol, id_usuario)
    
    def eliminar_usuario(self, id_usuario):
        return self.model.eliminar_usuario(id_usuario)