from models.login_model import LoginModel

class LoginController:
    def __init__(self):
        self.model = LoginModel()
    
    def verificar_credenciales(self, usuario, contrasena):
        return self.model.verificar_credenciales(usuario, contrasena)