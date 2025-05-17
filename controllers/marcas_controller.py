from models.marcas_model import MarcasModel

class MarcasController:
    def __init__(self):
        self.model = MarcasModel()

    def obtener_marcas(self):
        return self.model.obtener_marcas()

    def obtener_proveedores(self):
        return self.model.obtener_proveedores()

    def agregar_marca(self, nombre, rfc):
        return self.model.agregar_marca(nombre, rfc)

    def actualizar_marca(self, id_marca, nombre, rfc):
        return self.model.actualizar_marca(id_marca, nombre, rfc)

    def eliminar_marca(self, id_marca):
        return self.model.eliminar_marca(id_marca)