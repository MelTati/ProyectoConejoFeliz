from models.detalles_ventas_models import DetallesVentasModel
from PyQt6.QtCore import pyqtSignal, QObject

class DetallesVentasController(QObject):
    detalle_modificado = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.model = DetallesVentasModel()
    
    def obtener_detalles_venta(self, id_venta):
        return self.model.obtener_detalles_venta(id_venta)
    
    def agregar_articulo(self, id_venta, codigo_articulo, cantidad, subtotal):
        try:
            resultado = self.model.agregar_articulo(id_venta, codigo_articulo, cantidad, subtotal)
            if resultado:
                self.detalle_modificado.emit()
            return resultado
        except Exception as e:
            raise e
    
    def eliminar_articulo(self, id_venta, codigo_articulo):
        try:
            resultado = self.model.eliminar_articulo(id_venta, codigo_articulo)
            if resultado:
                self.detalle_modificado.emit()
            return resultado
        except Exception as e:
            raise e
    
    def obtener_total_venta(self, id_venta):
        return self.model.obtener_total_venta(id_venta)
    
    def obtener_ultima_venta(self):
        return self.model.obtener_ultima_venta()
    
    def buscar_articulo(self, busqueda):
        return self.model.buscar_articulo(busqueda)