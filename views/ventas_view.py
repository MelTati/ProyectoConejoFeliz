from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QDateEdit, QLabel, QApplication
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIcon
from controllers.ventas_controllers import VentasController
from views.cliente_view import ClienteView
from views.detalles_ventas_views import VentanaDetallesVentas

class VentanaVentas(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = VentasController()
        self.setWindowTitle("Gestión de Ventas")
        self.resize(950, 400)
        self.init_ui()
        self.cargar_datos()
        self.controller.actualizar_ventas_signal.connect(self.cargar_datos)

    def init_ui(self):
        layout = QVBoxLayout()

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(8)
        self.tabla.setHorizontalHeaderLabels([
            "ID Venta", "Fecha Venta", "Usuario (Tel)", "Cliente (Tel)",
            "Código Artículo", "Nombre Artículo", "Cantidad", "Subtotal"
        ])
        self.tabla.cellClicked.connect(self.seleccionar_fila)
        layout.addWidget(self.tabla)

        # Formulario
        form_layout = QHBoxLayout()

        self.input_fecha = QDateEdit()
        self.input_fecha.setDisplayFormat("yyyy-MM-dd")
        self.input_fecha.setCalendarPopup(True)
        self.input_fecha.setSpecialValueText("Seleccione la fecha")
        self.input_fecha.setDateRange(QDate(1900, 1, 1), QDate(2100, 12, 31))
        self.input_fecha.setDate(self.input_fecha.minimumDate())
        self.input_fecha.setStyleSheet("QDateEdit { border: 1px solid #B0B0B0; border-radius: 10px; padding: 5px; }")
        form_layout.addWidget(self.input_fecha)

        self.combo_usuarios = QComboBox()
        self.combo_usuarios.setPlaceholderText("Seleccione un usuario")
        self.combo_usuarios.setStyleSheet("QComboBox { border: 1px solid #B0B0B0; border-radius: 10px; padding: 5px; }")
        form_layout.addWidget(self.combo_usuarios)

        self.combo_clientes = QComboBox()
        self.combo_clientes.setPlaceholderText("Seleccione un cliente")
        self.combo_clientes.setStyleSheet("QComboBox { border: 1px solid #B0B0B0; border-radius: 10px; padding: 5px; }")
        form_layout.addWidget(self.combo_clientes)

        layout.addLayout(form_layout)

        # Botones
        botones_layout = QHBoxLayout()

        btn_estilo = """
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 8px 18px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #1c5980;
        }
        """

        btn_agregar = QPushButton(" Agregar")
        btn_agregar.setIcon(QIcon("icons/add.png"))
        btn_actualizar = QPushButton(" Actualizar")
        btn_actualizar.setIcon(QIcon("icons/update.png"))
        btn_eliminar = QPushButton(" Eliminar")
        btn_eliminar.setIcon(QIcon("icons/delete.png"))
        btn_detalles = QPushButton(" Detalles")
        btn_detalles.setIcon(QIcon("icons/details.png"))

        for btn in [btn_agregar, btn_actualizar, btn_eliminar, btn_detalles]:
            btn.setStyleSheet(btn_estilo)

        btn_agregar.clicked.connect(self.agregar_venta)
        btn_actualizar.clicked.connect(self.actualizar_venta)
        btn_eliminar.clicked.connect(self.eliminar_venta)
        btn_detalles.clicked.connect(self.abrir_detalles_venta)

        botones_layout.addWidget(btn_agregar)
        botones_layout.addWidget(btn_actualizar)
        botones_layout.addWidget(btn_eliminar)
        botones_layout.addWidget(btn_detalles)

        self.boton_clientes = QPushButton(" Clientes")
        self.boton_clientes.setIcon(QIcon("icons/clients.png"))
        self.boton_clientes.setStyleSheet(btn_estilo)
        self.boton_clientes.clicked.connect(self.abrir_clientes)
        layout.addWidget(self.boton_clientes)
        layout.addLayout(botones_layout)
        self.setLayout(layout)

    def abrir_clientes(self):
        self.ventana_clientes = ClienteView()
        self.ventana_clientes.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.ventana_clientes.show()

    def abrir_detalles_venta(self):
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione una venta para ver sus detalles.")
            return

        venta_id = int(self.tabla.item(fila_seleccionada, 0).text())
        
        if hasattr(self, 'detalles_ventas'):
            self.detalles_ventas.close()
        
        self.detalles_ventas = VentanaDetallesVentas(venta_id)
        self.detalles_ventas.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.detalles_ventas.detalle_modificado.connect(
            lambda: self.actualizar_fila_venta(venta_id))
        self.detalles_ventas.show()

    def actualizar_fila_venta(self, venta_id):
        fila = -1
        for row in range(self.tabla.rowCount()):
            if int(self.tabla.item(row, 0).text()) == venta_id:
                fila = row
                break
        
        if fila == -1:
            return

        venta = self.controller.obtener_detalles_venta(venta_id)
        if venta:
            self.tabla.setItem(fila, 1, QTableWidgetItem(str(venta["fecha_venta"])))
            self.tabla.setItem(fila, 4, QTableWidgetItem(str(venta["codigo_articulo"] or "")))
            self.tabla.setItem(fila, 5, QTableWidgetItem(venta["nombre_articulo"] or ""))
            self.tabla.setItem(fila, 6, QTableWidgetItem(str(venta["cantidad"] or "")))
            self.tabla.setItem(fila, 7, QTableWidgetItem(str(venta["subtotal"] or "")))

            totales = self.controller.obtener_totales_venta(venta_id)
            if totales["total_articulos"] > 1:
                tooltip = f"Total artículos: {totales['total_articulos']}\nTotal venta: ${totales['total_venta']:.2f}"
                for col in range(4, 8):
                    if self.tabla.item(fila, col):
                        self.tabla.item(fila, col).setToolTip(tooltip)
        
        QApplication.processEvents()

    def cargar_datos(self):
        try:
            # Cargar usuarios
            usuarios = self.controller.obtener_usuarios()
            self.combo_usuarios.clear()
            for usuario in usuarios:
                self.combo_usuarios.addItem(
                    f"{usuario['nombre_usuario']} ({usuario['telefono']}) - {usuario['cargo']}",
                    usuario["id_usuario"]
                )

            # Cargar clientes
            clientes = self.controller.obtener_clientes()
            self.combo_clientes.clear()
            for cliente in clientes:
                self.combo_clientes.addItem(
                    f"{cliente['nombre']} ({cliente['telefono']})",
                    cliente["id_cliente"]
                )

            # Cargar ventas
            resultados = self.controller.obtener_ventas()

            self.tabla.setRowCount(0)
            for fila_num, venta in enumerate(resultados):
                self.tabla.insertRow(fila_num)
                self.tabla.setItem(fila_num, 0, QTableWidgetItem(str(venta["id_ventas"])))
                self.tabla.setItem(fila_num, 1, QTableWidgetItem(str(venta["fecha_venta"])))
                self.tabla.setItem(fila_num, 2, QTableWidgetItem(f"{venta['nombre_usuario']} ({venta['telefono_usuario']})"))
                self.tabla.setItem(fila_num, 3, QTableWidgetItem(f"{venta['nombre_cliente']} ({venta['telefono_cliente']})"))
                self.tabla.setItem(fila_num, 4, QTableWidgetItem(str(venta["codigo_articulo"] or "")))
                self.tabla.setItem(fila_num, 5, QTableWidgetItem(venta["nombre_articulo"] or ""))
                self.tabla.setItem(fila_num, 6, QTableWidgetItem(str(venta["cantidad"] or "")))
                self.tabla.setItem(fila_num, 7, QTableWidgetItem(str(venta["subtotal"] or "")))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la tabla: {e}")

    def seleccionar_fila(self, fila, _):
        self.input_fecha.setDate(QDate.fromString(self.tabla.item(fila, 1).text(), "yyyy-MM-dd"))

        usuario_texto = self.tabla.item(fila, 2).text().split(" (")[0]
        cliente_texto = self.tabla.item(fila, 3).text().split(" (")[0]

        index_usuario = self.combo_usuarios.findText(usuario_texto, Qt.MatchFlag.MatchStartsWith)
        index_cliente = self.combo_clientes.findText(cliente_texto, Qt.MatchFlag.MatchStartsWith)

        if index_usuario != -1:
            self.combo_usuarios.setCurrentIndex(index_usuario)
        if index_cliente != -1:
            self.combo_clientes.setCurrentIndex(index_cliente)
    
    def validar_campos(self):
        if self.input_fecha.date() == self.input_fecha.minimumDate():
            QMessageBox.warning(self, "Advertencia", "Seleccione una fecha válida.")
            return False
        return True

    def agregar_venta(self):
        if not self.validar_campos():
            return
        
        success, message = self.controller.agregar_venta(
            self.input_fecha.date().toString("yyyy-MM-dd"),
            self.combo_usuarios.currentData(),
            self.combo_clientes.currentData()
        )
        
        if success:
            QMessageBox.information(self, "Éxito", message)
        else:
            QMessageBox.critical(self, "Error", message)

    def actualizar_venta(self):
        if not self.validar_campos():
            return
        
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione una venta para actualizar.")
            return

        venta_id = int(self.tabla.item(fila_seleccionada, 0).text())
        
        success, message = self.controller.actualizar_venta(
            self.input_fecha.date().toString("yyyy-MM-dd"),
            self.combo_usuarios.currentData(),
            self.combo_clientes.currentData(),
            venta_id
        )
        
        if success:
            QMessageBox.information(self, "Éxito", message)
        else:
            QMessageBox.critical(self, "Error", message)

    def eliminar_venta(self):
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione una venta para eliminar.")
            return

        venta_id_item = self.tabla.item(fila_seleccionada, 0)
        if venta_id_item is None:
            QMessageBox.warning(self, "Advertencia", "No se pudo obtener el ID de la venta.")
            return

        venta_id = int(venta_id_item.text())

        confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro de eliminar la venta #{venta_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmacion == QMessageBox.StandardButton.Yes:
            success, message = self.controller.eliminar_venta(venta_id)
            if success:
                QMessageBox.information(self, "Éxito", message)
            else:
                QMessageBox.critical(self, "Error", message)