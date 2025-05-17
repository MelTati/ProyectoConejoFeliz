from models.categorias_model import CategoriaModel

class CategoriaController:
    @staticmethod
    def obtener_categorias():
        return CategoriaModel.obtener_todas()

    @staticmethod
    def agregar_categoria(tipo_categoria):
        return CategoriaModel.agregar(tipo_categoria)

    @staticmethod
    def actualizar_categoria(id_categoria, tipo_categoria):
        return CategoriaModel.actualizar(id_categoria, tipo_categoria)

    @staticmethod
    def eliminar_categoria(id_categoria):
        return CategoriaModel.eliminar(id_categoria)