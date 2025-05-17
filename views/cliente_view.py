from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from controllers.cliente_controller import ClienteController

class ClienteView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ClienteController()
        self.setWindowTitle("Gestión de Clientes")
        self.resize(600, 400)
        self.init_ui()
        self.cargar_datos()

    def init_ui(self):
        layout = QVBoxLayout()

        # Tabla de clientes
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Teléfono"])
        self.tabla.cellClicked.connect(self.seleccionar_fila)
        layout.addWidget(self.tabla)

        # Campos de entrada
        form_layout = QHBoxLayout()
        self.input_nombre = QLineEdit()
        self.input_telefono = QLineEdit()

        self.input_nombre.setPlaceholderText("Nombre")
        self.input_telefono.setPlaceholderText("Teléfono")

        form_layout.addWidget(self.input_nombre)
        form_layout.addWidget(self.input_telefono)
        layout.addLayout(form_layout)

        # Botones
        botones_layout = QHBoxLayout()
        btn_agregar = QPushButton("Agregar")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")

        btn_agregar.clicked.connect(self.agregar_cliente)
        btn_actualizar.clicked.connect(self.actualizar_cliente)
        btn_eliminar.clicked.connect(self.eliminar_cliente)

        botones_layout.addWidget(btn_agregar)
        botones_layout.addWidget(btn_actualizar)
        botones_layout.addWidget(btn_eliminar)
        layout.addLayout(botones_layout)

        self.setLayout(layout)

    def cargar_datos(self):
        clientes = self.controller.obtener_clientes()
        self.tabla.setRowCount(0)
        for fila_num, cliente in enumerate(clientes):
            self.tabla.insertRow(fila_num)
            self.tabla.setItem(fila_num, 0, QTableWidgetItem(str(cliente["id_cliente"])))
            self.tabla.setItem(fila_num, 1, QTableWidgetItem(cliente["nombre"] or ""))
            self.tabla.setItem(fila_num, 2, QTableWidgetItem(cliente["telefono"] or ""))

    def seleccionar_fila(self, fila, _):
        self.id_seleccionado = int(self.tabla.item(fila, 0).text())
        self.input_nombre.setText(self.tabla.item(fila, 1).text())
        self.input_telefono.setText(self.tabla.item(fila, 2).text())

    def agregar_cliente(self):
        nombre = self.input_nombre.text()
        telefono = self.input_telefono.text()
        
        if self.controller.agregar_cliente(nombre, telefono):
            self.cargar_datos()
            self.input_nombre.clear()
            self.input_telefono.clear()

    def actualizar_cliente(self):
        if not hasattr(self, "id_seleccionado"):
            QMessageBox.warning(self, "Advertencia", "Seleccione un cliente de la tabla.")
            return
            
        nombre = self.input_nombre.text()
        telefono = self.input_telefono.text()
        
        if self.controller.actualizar_cliente(self.id_seleccionado, nombre, telefono):
            self.cargar_datos()

    def eliminar_cliente(self):
        if not hasattr(self, "id_seleccionado"):
            QMessageBox.warning(self, "Advertencia", "Seleccione un cliente de la tabla.")
            return
            
        if self.controller.eliminar_cliente(self.id_seleccionado):
            self.cargar_datos()
            self.input_nombre.clear()
            self.input_telefono.clear()
            delattr(self, "id_seleccionado")