from models.ticket_model import TicketModel
from PyQt6.QtWidgets import QMessageBox

class TicketController:
    def __init__(self):
        self.model = TicketModel()

    def obtener_todos_tickets(self):
        try:
            return self.model.obtener_todos()
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudieron cargar los tickets: {e}")
            return []

    def obtener_modos_pago(self):
        try:
            return self.model.obtener_modos_pago()
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudieron cargar los modos de pago: {e}")
            return []

    def obtener_ventas(self):
        try:
            return self.model.obtener_ventas()
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudieron cargar las ventas: {e}")
            return []

    def crear_ticket(self, id_ticket, id_modo_pago, id_ventas):
        try:
            return self.model.crear_ticket(id_ticket, id_modo_pago, id_ventas)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo crear el ticket: {e}")
            return False

    def actualizar_ticket(self, id_ticket, id_modo_pago, id_ventas):
        try:
            return self.model.actualizar_ticket(id_ticket, id_modo_pago, id_ventas)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo actualizar el ticket: {e}")
            return False

    def eliminar_ticket(self, id_ticket):
        try:
            return self.model.eliminar_ticket(id_ticket)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo eliminar el ticket: {e}")
            return False

    def obtener_detalles_impresion(self, id_ticket):
        try:
            return self.model.obtener_detalles_impresion(id_ticket)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudieron obtener los detalles: {e}")
            return []