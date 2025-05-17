import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QComboBox
)
from controllers.marcas_controller import MarcasController

class MarcasView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = MarcasController()
        self.setWindowTitle("Gestión de Marcas")
        self.resize(500, 300)
        self.init_ui()
        self.cargar_proveedores()
        self.cargar_datos()

    def init_ui(self):
        layout = QVBoxLayout()

        # Tabla de marcas
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID Marca", "Nombre", "Proveedor"])
        self.tabla.cellClicked.connect(self.seleccionar_fila)
        layout.addWidget(self.tabla)

        # Formulario
        form_layout = QHBoxLayout()
        self.input_nombre = QLineEdit()
        self.combo_proveedor = QComboBox()
        self.input_nombre.setPlaceholderText("Nombre de la Marca")

        form_layout.addWidget(self.input_nombre)
        form_layout.addWidget(self.combo_proveedor)
        layout.addLayout(form_layout)

        # Botones
        botones_layout = QHBoxLayout()
        btn_agregar = QPushButton("Agregar")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")

        btn_agregar.clicked.connect(self.agregar_marca)
        btn_actualizar.clicked.connect(self.actualizar_marca)
        btn_eliminar.clicked.connect(self.eliminar_marca)

        botones_layout.addWidget(btn_agregar)
        botones_layout.addWidget(btn_actualizar)
        botones_layout.addWidget(btn_eliminar)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

    def cargar_proveedores(self):
        self.combo_proveedor.clear()
        proveedores = self.controller.obtener_proveedores()
        for prov in proveedores:
            self.combo_proveedor.addItem(prov["nombre_proveedor"], prov["RFC"])

    def cargar_datos(self):
        try:
            resultados = self.controller.obtener_marcas()
            self.tabla.setRowCount(0)
            for fila_num, marca in enumerate(resultados):
                self.tabla.insertRow(fila_num)
                self.tabla.setItem(fila_num, 0, QTableWidgetItem(str(marca["id_marca"])))
                self.tabla.setItem(fila_num, 1, QTableWidgetItem(marca["nombre_marca"] or ""))
                self.tabla.setItem(fila_num, 2, QTableWidgetItem(marca["nombre_proveedor"] or ""))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la tabla: {e}")

    def seleccionar_fila(self, fila, _):
        self.id_marca_seleccionada = int(self.tabla.item(fila, 0).text())
        self.input_nombre.setText(self.tabla.item(fila, 1).text())
        nombre_proveedor = self.tabla.item(fila, 2).text()
        index = self.combo_proveedor.findText(nombre_proveedor)
        if index != -1:
            self.combo_proveedor.setCurrentIndex(index)

    def validar_campos(self):
        if not self.input_nombre.text().strip():
            QMessageBox.warning(self, "Advertencia", "El nombre de la marca no puede estar vacío.")
            return False
        if self.combo_proveedor.currentIndex() == -1:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un proveedor.")
            return False
        return True

    def agregar_marca(self):
        if not self.validar_campos():
            return
        try:
            nombre = self.input_nombre.text().strip()
            rfc = self.combo_proveedor.currentData()
            if self.controller.agregar_marca(nombre, rfc):
                QMessageBox.information(self, "Éxito", "Marca agregada correctamente.")
                self.cargar_datos()
                self.limpiar_campos()
            else:
                QMessageBox.critical(self, "Error", "No se pudo agregar la marca.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar la marca: {e}")

    def actualizar_marca(self):
        if not self.validar_campos() or not hasattr(self, "id_marca_seleccionada"):
            QMessageBox.warning(self, "Advertencia", "Seleccione una marca de la tabla para actualizar.")
            return
        try:
            nombre = self.input_nombre.text().strip()
            rfc = self.combo_proveedor.currentData()
            if self.controller.actualizar_marca(self.id_marca_seleccionada, nombre, rfc):
                QMessageBox.information(self, "Éxito", "Marca actualizada correctamente.")
                self.cargar_datos()
                self.limpiar_campos()
            else:
                QMessageBox.critical(self, "Error", "No se pudo actualizar la marca.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar la marca: {e}")

    def eliminar_marca(self):
        if not hasattr(self, "id_marca_seleccionada"):
            QMessageBox.warning(self, "Advertencia", "Seleccione una marca para eliminar.")
            return
        confirmacion = QMessageBox.question(
            self, "Confirmar eliminación",
            "¿Está seguro de eliminar esta marca?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmacion == QMessageBox.StandardButton.Yes:
            try:
                if self.controller.eliminar_marca(self.id_marca_seleccionada):
                    QMessageBox.information(self, "Éxito", "Marca eliminada correctamente.")
                    self.cargar_datos()
                    self.limpiar_campos()
                else:
                    QMessageBox.critical(self, "Error", "No se pudo eliminar la marca.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar la marca: {e}")

    def limpiar_campos(self):
        self.input_nombre.clear()
        self.combo_proveedor.setCurrentIndex(-1)
        if hasattr(self, "id_marca_seleccionada"):
            del self.id_marca_seleccionada