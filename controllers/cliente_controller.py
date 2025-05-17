from models.cliente_model import ClienteModel
from PyQt6.QtWidgets import QMessageBox

class ClienteController:
    def __init__(self):
        self.model = ClienteModel()

    def obtener_clientes(self):
        try:
            return self.model.obtener_clientes()
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudieron obtener los clientes: {e}")
            return []
    
    def agregar_cliente(self, nombre, telefono):
        try:
            if not nombre.strip() or not telefono.strip():
                QMessageBox.warning(None, "Advertencia", "Por favor complete todos los campos.")
                return False
            
            self.model.agregar_cliente(nombre.strip(), telefono.strip())
            QMessageBox.information(None, "Éxito", "Cliente agregado correctamente")
            return True
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo agregar el cliente: {e}")
            return False

    def actualizar_cliente(self, id_cliente, nombre, telefono):
        try:
            if not nombre.strip() or not telefono.strip():
                QMessageBox.warning(None, "Advertencia", "Por favor complete todos los campos.")
                return False
            
            self.model.actualizar_cliente(id_cliente, nombre.strip(), telefono.strip())
            QMessageBox.information(None, "Éxito", "Cliente actualizado correctamente")
            return True
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo actualizar el cliente: {e}")
            return False

    def eliminar_cliente(self, id_cliente):
        try:
            self.model.eliminar_cliente(id_cliente)
            QMessageBox.information(None, "Éxito", "Cliente eliminado correctamente")
            return True
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo eliminar el cliente: {e}")
            return False