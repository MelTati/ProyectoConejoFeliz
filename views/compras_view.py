from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QLabel, QLineEdit, QDateEdit, QMessageBox, QApplication
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon
from controllers.compras_controller import ComprasController

class VentanaCompras(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Compras")
        self.resize(1000, 500)
        self.setWindowIcon(QIcon("icons/shopping-cart.png"))

        self.controller = ComprasController()
        self.init_ui()
        self.cargar_comboboxes()
        self.cargar_compras()

    def init_ui(self):
        layout = QVBoxLayout()

        # --- Filtros ---
        filtros = QHBoxLayout()

        self.combo_proveedor = QComboBox()
        filtros.addWidget(QLabel("Proveedor:"))
        filtros.addWidget(self.combo_proveedor)

        self.fecha_compra = QDateEdit(QDate.currentDate())
        self.fecha_compra.setCalendarPopup(True)
        filtros.addWidget(QLabel("Fecha:"))
        filtros.addWidget(self.fecha_compra)

        self.input_codigo = QLineEdit()
        self.input_codigo.setPlaceholderText("ID de Compra")
        filtros.addWidget(QLabel("ID:"))
        filtros.addWidget(self.input_codigo)

        btn_agregar = QPushButton("Agregar")
        btn_agregar.clicked.connect(self.agregar_compra)
        filtros.addWidget(btn_agregar)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.eliminar_compra)
        filtros.addWidget(btn_eliminar)

        btn_detalles = QPushButton("Ver Detalles")
        btn_detalles.clicked.connect(self.ver_detalles)
        filtros.addWidget(btn_detalles)

        layout.addLayout(filtros)

        # --- Tabla ---
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Proveedor", "Fecha", "Subtotal"])
        layout.addWidget(self.tabla)

        self.setLayout(layout)

    def cargar_comboboxes(self):
        self.combo_proveedor.clear()
        for proveedor in self.controller.obtener_proveedores():
            self.combo_proveedor.addItem(proveedor["nombre_proveedor"], proveedor["RFC"])

    def cargar_compras(self):
        self.tabla.setRowCount(0)
        for fila, compra in enumerate(self.controller.obtener_compras()):
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(compra["id_compras"])))
            self.tabla.setItem(fila, 1, QTableWidgetItem(compra["nombre_proveedor"]))
            self.tabla.setItem(fila, 2, QTableWidgetItem(str(compra["fecha_compras"])))
            self.tabla.setItem(fila, 3, QTableWidgetItem(f"${compra['total']:.2f}"))

    def agregar_compra(self):
        id_compra = self.input_codigo.text().strip()
        rfc = self.combo_proveedor.currentData()
        fecha = self.fecha_compra.date().toString("yyyy-MM-dd")

        if not id_compra:
            QMessageBox.warning(self, "Error", "Ingrese un ID de compra")
            return

        try:
            self.controller.agregar_compra(id_compra, rfc, fecha)
            self.cargar_compras()
            QMessageBox.information(self, "Éxito", "Compra registrada")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar: {str(e)}")

    def eliminar_compra(self):
        fila = self.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccione una compra")
            return

        id_compra = self.tabla.item(fila, 0).text()
        if QMessageBox.question(self, "Confirmar", "¿Eliminar compra?") == QMessageBox.StandardButton.Yes:
            try:
                self.controller.eliminar_compra(id_compra)
                self.cargar_compras()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar: {str(e)}")

    def ver_detalles(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Advertencia", "Selecciona una compra para ver detalles")
            return

        id_compra = int(self.tabla.item(fila, 0).text())
        
        # ÚNICA IMPORTACIÓN DE DETALLES_COMPRAS_VIEW
        from views.detalles_compras_view import VentanaDetallesCompras
        
        self.detalle_ventana = VentanaDetallesCompras(id_compras=id_compra)
        self.detalle_ventana.show()
