from models.articulo_model import ArticuloModel

class ArticuloController:
    def __init__(self, view):
        self.view = view
        self.model = ArticuloModel()

    def cargar_datos(self, filtros):
        return self.model.obtener_articulos(filtros)

    def cargar_categorias(self):
        return self.model.obtener_categorias()

    def cargar_marcas(self):
        return self.model.obtener_marcas()

    def agregar_articulo(self, datos):
        try:
            self.model.crear_articulo(datos)
        except Exception as e:
            raise ValueError(f"Error al agregar artículo: {e}")

    def actualizar_articulo(self, datos):
        try:
            self.model.actualizar_articulo(datos)
        except Exception as e:
            raise ValueError(f"Error al actualizar artículo: {e}")
    
    def eliminar_articulo(self, codigo):
        try:
            self.model.eliminar_articulo(codigo)
        except Exception as e:
            raise 
