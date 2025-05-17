from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QCheckBox, QComboBox, QLabel, QHeaderView
)
from PyQt6.QtGui import QColor
from controllers.articulo_controller import ArticuloController

class VentanaArticulos(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ArticuloController(self)
        self.codigo_seleccionado = None 
        self.init_ui()
        self.cargar_combos()
        self.cargar_datos()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Filtros
        filtro_layout = QHBoxLayout()

        self.buscador = QLineEdit()
        self.buscador.setPlaceholderText("Buscar por Código o Nombre...")
        self.buscador.textChanged.connect(self.cargar_datos) 

        self.filtro_categoria = QComboBox()
        self.filtro_categoria.currentIndexChanged.connect(self.cargar_datos)

        self.filtro_marca = QComboBox()
        self.filtro_marca.currentIndexChanged.connect(self.cargar_datos)

        filtro_layout.addWidget(QLabel("Buscar:"))
        filtro_layout.addWidget(self.buscador)
        filtro_layout.addWidget(QLabel("Filtrar por Categoría:"))
        filtro_layout.addWidget(self.filtro_categoria)
        filtro_layout.addWidget(QLabel("Filtrar por Marca:"))
        filtro_layout.addWidget(self.filtro_marca)
        layout.addLayout(filtro_layout)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(11)
        self.tabla.setHorizontalHeaderLabels([
            "Código", "Nombre", "Activo", "Precio", "Costo", "Categoría", 
            "Marca", "Descripción", "Cantidad_Minima","Cantidad_Maxima","Stock"
        ])
        self.tabla.cellClicked.connect(self.seleccionar_fila)
        layout.addWidget(self.tabla)

        # Ajuste de columnas
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(10, QHeaderView.ResizeMode.ResizeToContents)

        # Formulario
        form_layout = QHBoxLayout()
        self.input_codigo = QLineEdit()
        self.input_nombre = QLineEdit()
        self.checkbox_activado = QCheckBox("¿Activo?")
        self.input_precio = QLineEdit()
        self.input_costo = QLineEdit()
        self.combo_categoria = QComboBox()
        self.combo_marca = QComboBox()
        self.input_descripcion = QLineEdit()
        self.input_cantidad_maxima = QLineEdit()
        self.input_cantidad_minima = QLineEdit()
        self.stock = QLineEdit()

        self.input_codigo.setPlaceholderText("Código")
        self.input_nombre.setPlaceholderText("Nombre")
        self.input_precio.setPlaceholderText("Precio")
        self.input_costo.setPlaceholderText("Costo")
        self.input_descripcion.setPlaceholderText("Descripción")
        self.input_cantidad_maxima.setPlaceholderText("Cantidad máxima")
        self.input_cantidad_minima.setPlaceholderText("Cantidad mínima")
        self.stock.setPlaceholderText("Stock")

        form_layout.addWidget(self.input_codigo)
        form_layout.addWidget(self.input_nombre)
        form_layout.addWidget(self.checkbox_activado)
        form_layout.addWidget(self.input_precio)
        form_layout.addWidget(self.input_costo)
        form_layout.addWidget(self.combo_categoria)
        form_layout.addWidget(self.combo_marca)
        form_layout.addWidget(self.input_descripcion)
        form_layout.addWidget(self.input_cantidad_maxima)
        form_layout.addWidget(self.input_cantidad_minima)
        form_layout.addWidget(self.stock)
        layout.addLayout(form_layout)

        # Botones
        botones_layout = QHBoxLayout()
        btn_agregar = QPushButton("Agregar")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")

        btn_agregar.clicked.connect(self.agregar_articulo)
        btn_actualizar.clicked.connect(self.actualizar_articulo)
        btn_eliminar.clicked.connect(self.eliminar_articulo)

        botones_layout.addWidget(btn_agregar)
        botones_layout.addWidget(btn_actualizar)
        botones_layout.addWidget(btn_eliminar)
        layout.addLayout(botones_layout)
        
        self.setLayout(layout)

    def cargar_combos(self):
        # Cargar categorías y marcas
        try:
            categorias = self.controller.cargar_categorias()
            marcas = self.controller.cargar_marcas()
            print("Categorías cargadas:", categorias)
            print("Marcas cargadas:", marcas)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar categorías o marcas:\n{str(e)}")
            categorias = []
            marcas = []
        
        # Cargar combos de asignación
        self.combo_categoria.clear()
        for cat in categorias:
            self.combo_categoria.addItem(cat["tipo_categoria"], cat["id_categorias"])
            
        self.combo_marca.clear()
        for marca in marcas:
            self.combo_marca.addItem(marca["nombre_marca"], marca["id_marca"])
            
        # Cargar combos de filtro
        self.filtro_categoria.clear()
        self.filtro_categoria.addItem("Todas", None)
        for cat in categorias:
            self.filtro_categoria.addItem(cat["tipo_categoria"], cat["id_categorias"])
            
        self.filtro_marca.clear()
        self.filtro_marca.addItem("Todas", None)
        for marca in marcas:
            self.filtro_marca.addItem(marca["nombre_marca"], marca["id_marca"])

    def cargar_datos(self):
        try:
            categoria_id = self.filtro_categoria.currentData()
            marca_id = self.filtro_marca.currentData()
            texto_busqueda = self.buscador.text().strip()
            texto_busqueda_wildcard = f"%{texto_busqueda}%"
            
            filtros = (categoria_id, categoria_id, marca_id, marca_id, 
                      texto_busqueda_wildcard, texto_busqueda_wildcard)
            
            resultados = self.controller.cargar_datos(filtros)
            print("Resultados cargados:", resultados)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos:\n{str(e)}")
            resultados = []
        
        self.tabla.setRowCount(0)
        articulos_stock_bajo = []

        for fila, art in enumerate(resultados):
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila, 0, QTableWidgetItem(art["codigo_articulo"]))
            self.tabla.setItem(fila, 1, QTableWidgetItem(art["nombre_articulo"] or ""))
            self.tabla.setItem(fila, 2, QTableWidgetItem("Sí" if art["activacion_articulo"] else "No"))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(art["precio_articulo"])))
            self.tabla.setItem(fila, 4, QTableWidgetItem(str(art["costo_articulo"])))
            self.tabla.setItem(fila, 5, QTableWidgetItem(art["tipo_categoria"]))
            self.tabla.setItem(fila, 6, QTableWidgetItem(art["nombre_marca"]))
            self.tabla.setItem(fila, 7, QTableWidgetItem(art["descr_caracteristicas"] or ""))
            self.tabla.setItem(fila, 8, QTableWidgetItem(str(art["cantidad_maxima"])))
            self.tabla.setItem(fila, 9, QTableWidgetItem(str(art["cantidad_minima"])))

            # Stock y color
            item_stock = QTableWidgetItem(str(art["stock"]))
            stock = art["stock"]
            cantidad_minima = art["cantidad_minima"]

            if stock > cantidad_minima:
                item_stock.setBackground(QColor("lightblue"))
            elif stock == cantidad_minima:
                item_stock.setBackground(QColor("yellow"))   
                articulos_stock_bajo.append(f'{art["nombre_articulo"]} (Stock: {stock})')
            else:
                item_stock.setBackground(QColor("red")) 
                articulos_stock_bajo.append(f'{art["nombre_articulo"]} (Stock: {stock})')

            self.tabla.setItem(fila, 10, item_stock)

        # Mostrar advertencia si se está filtrando
        se_esta_filtrando = (
            categoria_id is not None or 
            marca_id is not None or 
            texto_busqueda != ""
        )

        if se_esta_filtrando and articulos_stock_bajo:
            mensaje = "Los siguientes artículos tienen stock bajo o crítico:\n\n"
            mensaje += "\n".join(articulos_stock_bajo)
            QMessageBox.warning(self, "Stock bajo", mensaje)

    def seleccionar_fila(self, fila, _):
        self.codigo_seleccionado = self.tabla.item(fila, 0).text()
        self.input_codigo.setText(self.codigo_seleccionado)
        self.input_nombre.setText(self.tabla.item(fila, 1).text())
        self.checkbox_activado.setChecked(self.tabla.item(fila, 2).text() == "Sí")
        self.input_precio.setText(self.tabla.item(fila, 3).text())
        self.input_costo.setText(self.tabla.item(fila, 4).text())
        
        # Buscar y seleccionar la categoría y marca en los combos
        categoria_texto = self.tabla.item(fila, 5).text()
        marca_texto = self.tabla.item(fila, 6).text()
        
        index_categoria = self.combo_categoria.findText(categoria_texto)
        if index_categoria >= 0:
            self.combo_categoria.setCurrentIndex(index_categoria)
            
        index_marca = self.combo_marca.findText(marca_texto)
        if index_marca >= 0:
            self.combo_marca.setCurrentIndex(index_marca)
            
        self.input_descripcion.setText(self.tabla.item(fila, 7).text())
        self.input_cantidad_maxima.setText(self.tabla.item(fila, 8).text())
        self.input_cantidad_minima.setText(self.tabla.item(fila, 9).text())
        self.stock.setText(self.tabla.item(fila, 10).text())

    def validar_campos(self):
        if (not self.input_codigo.text().strip() or
            not self.input_nombre.text().strip() or
            not self.input_precio.text().strip() or
            not self.input_costo.text().strip() or
            not self.input_cantidad_maxima.text().strip() or
            not self.input_cantidad_minima.text().strip() or
            not self.stock.text().strip()):
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios")
            return False
            
        try:
            float(self.input_precio.text())
            float(self.input_costo.text())
            int(self.input_cantidad_maxima.text())
            int(self.input_cantidad_minima.text())
            int(self.stock.text())
        except ValueError:
            QMessageBox.warning(self, "Advertencia", "Los campos numéricos deben contener valores válidos")
            return False
            
        if self.combo_categoria.currentIndex() == -1 or self.combo_marca.currentIndex() == -1:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una categoría y una marca")
            return False
            
        return True

    def agregar_articulo(self):
        if not self.validar_campos():
            return
            
        datos = (
            self.input_codigo.text().strip(),
            self.input_nombre.text().strip(),
            1 if self.checkbox_activado.isChecked() else 0,
            float(self.input_precio.text()),
            float(self.input_costo.text()),
            self.combo_categoria.currentData(),
            self.combo_marca.currentData(),
            self.input_descripcion.text().strip(),
            int(self.input_cantidad_maxima.text()),
            int(self.input_cantidad_minima.text()),
            int(self.stock.text())
        )
        
        try:
            self.controller.agregar_articulo(datos)
            QMessageBox.information(self, "Éxito", "Artículo agregado correctamente")
            self.cargar_datos()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar el artículo: {str(e)}")

    def actualizar_articulo(self):
        if not self.validar_campos():
            return
            
        if not self.codigo_seleccionado:
            QMessageBox.warning(self, "Advertencia", "Seleccione un artículo para actualizar")
            return

        datos = (
            self.input_nombre.text().strip(),
            1 if self.checkbox_activado.isChecked() else 0,
            float(self.input_precio.text()),
            float(self.input_costo.text()),
            self.combo_categoria.currentData(),
            self.combo_marca.currentData(),
            self.input_descripcion.text().strip(),
            int(self.input_cantidad_maxima.text()),
            int(self.input_cantidad_minima.text()),
            int(self.stock.text()),
            self.codigo_seleccionado
        )
        
        try:
            self.controller.actualizar_articulo(datos)
            QMessageBox.information(self, "Éxito", "Artículo actualizado correctamente")
            self.cargar_datos()
            self.limpiar_campos()
            self.codigo_seleccionado = None
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el artículo: {str(e)}")

    def eliminar_articulo(self):
        if not hasattr(self, 'codigo_seleccionado') or not self.codigo_seleccionado:
            QMessageBox.warning(self, "Advertencia", "Seleccione un artículo para eliminar")
            return
        
        try:
            # Confirmación antes de eliminar
            respuesta = QMessageBox.question(
                self, "Confirmar eliminación",
                "¿Está seguro de eliminar este artículo?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if respuesta == QMessageBox.StandardButton.Yes:
                self.controller.eliminar_articulo(self.codigo_seleccionado)
                QMessageBox.information(self, "Éxito", "Artículo eliminado correctamente")
                self.cargar_datos()
                self.limpiar_campos()
                
        except ValueError as e:
            QMessageBox.warning(self, "Advertencia", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar: {str(e)}")
            
    def limpiar_campos(self):
        self.input_codigo.clear()
        self.input_nombre.clear()
        self.checkbox_activado.setChecked(False)
        self.input_precio.clear()
        self.input_costo.clear()
        self.combo_categoria.setCurrentIndex(0)
        self.combo_marca.setCurrentIndex(0)
        self.input_descripcion.clear()
        self.input_cantidad_maxima.clear()
        self.input_cantidad_minima.clear()
        self.stock.clear()
