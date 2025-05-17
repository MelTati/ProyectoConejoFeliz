from models.proveedor_model import ProveedorModel

class ProveedorController:
    def __init__(self):
        self.model = ProveedorModel()

    def obtener_proveedores(self):
        return self.model.obtener_proveedores()

    def agregar_proveedor(self, rfc, nombre, direccion, telefono, email):
        return self.model.agregar_proveedor(rfc, nombre, direccion, telefono, email)

    def actualizar_proveedor(self, rfc, nombre, direccion, telefono, email):
        return self.model.actualizar_proveedor(rfc, nombre, direccion, telefono, email)

    def eliminar_proveedor(self, rfc):
        return self.model.eliminar_proveedor(rfc)