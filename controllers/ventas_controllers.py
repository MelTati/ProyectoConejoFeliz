from models.ventas_models import VentasModel
from PyQt6.QtCore import pyqtSignal, QObject

class VentasController(QObject):
    actualizar_ventas_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.model = VentasModel()
    
    def obtener_usuarios(self):
        return self.model.obtener_usuarios()
    
    def obtener_clientes(self):
        return self.model.obtener_clientes()
    
    def obtener_ventas(self):
        return self.model.obtener_ventas()
    
    def agregar_venta(self, fecha_venta, id_usuario, id_cliente):
        try:
            self.model.agregar_venta(fecha_venta, id_usuario, id_cliente)
            self.actualizar_ventas_signal.emit()
            return True, "Venta agregada correctamente"
        except Exception as e:
            return False, f"No se pudo agregar: {e}"
    
    def actualizar_venta(self, fecha_venta, id_usuario, id_cliente, id_ventas):
        try:
            self.model.actualizar_venta(fecha_venta, id_usuario, id_cliente, id_ventas)
            self.actualizar_ventas_signal.emit()
            return True, "Venta actualizada correctamente"
        except Exception as e:
            return False, f"No se pudo actualizar: {e}"
    
    def eliminar_venta(self, id_ventas):
        try:
            self.model.eliminar_venta(id_ventas)
            self.actualizar_ventas_signal.emit()
            return True, "Venta eliminada correctamente"
        except Exception as e:
            return False, f"No se pudo eliminar la venta: {e}"
    
    def obtener_detalles_venta(self, id_ventas):
        return self.model.obtener_detalles_venta(id_ventas)
    
    def obtener_totales_venta(self, id_ventas):
        return self.model.obtener_totales_venta(id_ventas)