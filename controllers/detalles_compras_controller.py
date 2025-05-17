# controllers/detalles_compras_controller.py
from models.detalles_compras_model import DetallesComprasModel
from PyQt6.QtCore import pyqtSignal, QObject

class DetallesComprasController(QObject):
    detalle_modificado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.model = DetallesComprasModel()

    def obtener_detalles_compra(self, id_compras):
        try:
            detalles = self.model.obtener_detalles_compra(id_compras)
            total = self.model.obtener_total_compra(id_compras)
            return detalles, total
        except Exception as e:
            raise e

    def agregar_articulo(self, id_compras, busqueda, cantidad):
        try:
            articulo = self.model.buscar_articulo(busqueda)
            if not articulo:
                raise Exception("Artículo no encontrado")
            
            if not id_compras:
                id_compras = self.model.obtener_ultima_compra()
                if not id_compras:
                    raise Exception("No hay compras registradas")
            
            self.model.agregar_articulo(id_compras, articulo["codigo_articulo"], cantidad)
            self.detalle_modificado.emit()
            return True
        except Exception as e:
            raise e

    def eliminar_articulo(self, id_compras, nombre_articulo):
        try:
            # Primero obtener el código del artículo por su nombre
            articulo = self.model.buscar_articulo(nombre_articulo)
            if not articulo:
                raise Exception("Artículo no encontrado")
            
            eliminado = self.model.eliminar_articulo(id_compras, articulo["codigo_articulo"])
            if eliminado:
                self.detalle_modificado.emit()
                return True
            return False
        except Exception as e:
            raise e

    def obtener_ultima_compra(self):
        try:
            return self.model.obtener_ultima_compra()
        except Exception as e:
            raise e

    def __del__(self):
        self.model.cerrar_conexion()