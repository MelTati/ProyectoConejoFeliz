# views/detalles_compras_view.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QSpinBox, QApplication, QLineEdit, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from controllers.detalles_compras_controller import DetallesComprasController

class VentanaDetallesCompras(QWidget):
    def __init__(self, id_compras=None):
        super().__init__()
        self.controller = DetallesComprasController()
        self.id_compras = id_compras
        self.setWindowTitle(f"Detalles de Compra #{self.id_compras}")
        self.resize(1000, 500)
        self.setWindowIcon(QIcon("icons/details.png"))

        if self.id_compras is None:
            self.id_compras = self.controller.obtener_ultima_compra()

        self.init_ui()
        self.cargar_datos()

        # Conectar señal de modificación
        self.controller.detalle_modificado.connect(self.cargar_datos)

    def init_ui(self):
        layout = QVBoxLayout()

        # Tabla de detalles
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels([
            "ID Compra", "Artículo", "Marca", "Categoría",
            "Precio Unitario", "Cantidad", "Subtotal"
        ])
        self.tabla.setColumnWidth(1, 200)
        self.tabla.setColumnWidth(2, 100)
        self.tabla.setColumnWidth(3, 120)
        layout.addWidget(self.tabla)

        # Formulario para agregar artículos
        form_layout = QHBoxLayout()

        self.input_codigo = QLineEdit()
        self.input_codigo.setPlaceholderText("Código o nombre del artículo")
        self.input_codigo.returnPressed.connect(self.buscar_articulo)
        form_layout.addWidget(self.input_codigo)

        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1, 999)
        self.spin_cantidad.setValue(1)
        form_layout.addWidget(QLabel("Cantidad:"))
        form_layout.addWidget(self.spin_cantidad)

        btn_agregar = QPushButton("Agregar")
        btn_agregar.clicked.connect(self.buscar_articulo)
        form_layout.addWidget(btn_agregar)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_eliminar.clicked.connect(self.eliminar_detalle)
        form_layout.addWidget(btn_eliminar)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def cargar_datos(self):
        if not self.id_compras:
            return

        try:
            detalles, total = self.controller.obtener_detalles_compra(self.id_compras)
            self.tabla.setRowCount(0)

            for fila, detalle in enumerate(detalles):
                self.tabla.insertRow(fila)
                self.tabla.setItem(fila, 0, QTableWidgetItem(str(detalle["id_compras"])))
                self.tabla.setItem(fila, 1, QTableWidgetItem(detalle["nombre_articulo"]))
                self.tabla.setItem(fila, 2, QTableWidgetItem(detalle["nombre_marca"]))
                self.tabla.setItem(fila, 3, QTableWidgetItem(detalle["tipo_categoria"]))
                self.tabla.setItem(fila, 4, QTableWidgetItem(f"${detalle['costo_articulo']:.2f}"))
                self.tabla.setItem(fila, 5, QTableWidgetItem(str(detalle["cantidad"])))
                self.tabla.setItem(fila, 6, QTableWidgetItem(f"${detalle['subtotal']:.2f}"))

            # Agregar fila de total
            self.tabla.insertRow(self.tabla.rowCount())
            fila_total = self.tabla.rowCount() - 1
            self.tabla.setItem(fila_total, 5, QTableWidgetItem("TOTAL:"))
            self.tabla.setItem(fila_total, 6, QTableWidgetItem(f"${total:.2f}"))
            self.tabla.item(fila_total, 6).setBackground(Qt.GlobalColor.lightGray)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los detalles: {e}")

    def buscar_articulo(self):
        entrada = self.input_codigo.text().strip()
        cantidad = self.spin_cantidad.value()

        if not entrada:
            QMessageBox.warning(self, "Advertencia", "Ingrese un código o nombre de artículo")
            return

        try:
            self.controller.agregar_articulo(self.id_compras, entrada, cantidad)
            self.input_codigo.clear()
            self.spin_cantidad.setValue(1)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def eliminar_detalle(self):
        fila = self.tabla.currentRow()
        if fila < 0 or fila >= self.tabla.rowCount() - 1:
            QMessageBox.warning(self, "Advertencia", "Seleccione un artículo para eliminar")
            return

        nombre_articulo = self.tabla.item(fila, 1).text()

        respuesta = QMessageBox.question(
            self, "Confirmar",
            f"¿Eliminar '{nombre_articulo}' de la compra?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            try:
                self.controller.eliminar_articulo(self.id_compras, nombre_articulo)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def closeEvent(self, event):
        self.controller.detalle_modificado.emit()
        event.accept()