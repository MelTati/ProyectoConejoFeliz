from models.compras_model import ComprasModel

class ComprasController:
    def __init__(self):
        self.model = ComprasModel()

    def agregar_compra(self, id_compras, rfc, fecha_compras):
        return self.model.crear_compra(id_compras, rfc, fecha_compras)

    def obtener_compras(self):
        return self.model.obtener_compras()

    def eliminar_compra(self, id_compras):
        return self.model.eliminar_compra(id_compras)

    def obtener_proveedores(self):
        return self.model.obtener_proveedores()