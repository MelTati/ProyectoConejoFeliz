from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, 
    QFileDialog, QLabel
)
from PyQt6.QtGui import QPainter, QFont, QPageSize, QPageLayout, QFontMetrics, QImage
from PyQt6.QtCore import QMarginsF, QSizeF, Qt
from PyQt6.QtPrintSupport import QPrinter
from PIL.ImageQt import ImageQt
from urllib.request import urlopen
import qrcode
from controllers.ticket_controller import TicketController

class TicketView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = TicketController()
        self.setWindowTitle("Gestión de Tickets")
        self.resize(1000, 500)
        self.init_ui()
        self.cargar_datos()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #E0F7FA,
                    stop: 1 #FFFFFF
                );
            }
        """)

        layout = QVBoxLayout()

        # Encabezado
        header = QLabel("🎟️ Gestión de Tickets")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #FFD700;
                text-shadow: 2px 2px 4px #000000;
            }
        """)
        layout.addWidget(header)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "ID Ticket", "Modo de Pago", "ID Venta", "Fecha Venta", "Usuario", "Cliente"
        ])
        self.tabla.cellClicked.connect(self.seleccionar_fila)
        layout.addWidget(self.tabla)

        # Campos de entrada
        form_layout = QHBoxLayout()
        self.input_id = QLineEdit()
        self.combo_pago = QComboBox()
        self.combo_ventas = QComboBox()

        self.input_id.setPlaceholderText("ID Ticket")
        self.input_id.setStyleSheet("""
            QLineEdit {
                border: 2px solid #FFD700;
                border-radius: 10px;
                padding: 5px;
                background-color: #FFFFFF;
            }
        """)
        self.combo_pago.setStyleSheet("""
            QComboBox {
                border: 2px solid #800080;
                border-radius: 10px;
                padding: 5px;
                background-color: #FFFFFF;
            }
        """)
        self.combo_ventas.setStyleSheet("""
            QComboBox {
                border: 2px solid #FF1493;
                border-radius: 10px;
                padding: 5px;
                background-color: #FFFFFF;
            }
        """)

        form_layout.addWidget(self.input_id)
        form_layout.addWidget(self.combo_pago)
        form_layout.addWidget(self.combo_ventas)
        layout.addLayout(form_layout)

        # Botones
        btn_layout = QHBoxLayout()
        btn_agregar = QPushButton("Agregar")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")
        btn_imprimir = QPushButton("Imprimir")

        btn_agregar.setStyleSheet("""
            QPushButton {
                background-color: #FFD700;
                color: #000000;
                border-radius: 15px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFC107;
            }
        """)
        btn_actualizar.setStyleSheet("""
            QPushButton {
                background-color: #800080;
                color: #FFFFFF;
                border-radius: 15px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #9A32CD;
            }
        """)
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #FF1493;
                color: #FFFFFF;
                border-radius: 15px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF69B4;
            }
        """)
        btn_imprimir.setStyleSheet("""
            QPushButton {
                background-color: #87CEFA;
                color: #000000;
                border-radius: 15px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00BFFF;
            }
        """)

        btn_agregar.clicked.connect(self.agregar_ticket)
        btn_actualizar.clicked.connect(self.actualizar_ticket)
        btn_eliminar.clicked.connect(self.eliminar_ticket)
        btn_imprimir.clicked.connect(self.generar_impresion)

        btn_layout.addWidget(btn_agregar)
        btn_layout.addWidget(btn_actualizar)
        btn_layout.addWidget(btn_eliminar)
        btn_layout.addWidget(btn_imprimir)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def cargar_datos(self):
        # Cargar modos de pago
        pagos = self.controller.obtener_modos_pago()
        self.combo_pago.clear()
        for pago in pagos:
            self.combo_pago.addItem(pago["tipo"], pago["id_modo_pago"])

        # Cargar ventas
        ventas = self.controller.obtener_ventas()
        self.combo_ventas.clear()
        for venta in ventas:
            texto = f'{venta["id_ventas"]} - {venta["fecha_venta"]} / {venta["nombre_usuario"]} / {venta["nombre_cliente"]}'
            self.combo_ventas.addItem(texto, venta["id_ventas"])

        # Cargar tickets
        tickets = self.controller.obtener_todos_tickets()
        self.tabla.setRowCount(0)
        for i, ticket in enumerate(tickets):
            self.tabla.insertRow(i)
            self.tabla.setItem(i, 0, QTableWidgetItem(str(ticket["id_ticket"])))
            self.tabla.setItem(i, 1, QTableWidgetItem(ticket["modo_pago"]))
            self.tabla.setItem(i, 2, QTableWidgetItem(str(ticket["id_ventas"])))
            self.tabla.setItem(i, 3, QTableWidgetItem(str(ticket["fecha_venta"])))
            self.tabla.setItem(i, 4, QTableWidgetItem(ticket["nombre_usuario"]))
            self.tabla.setItem(i, 5, QTableWidgetItem(ticket["nombre_cliente"]))

    def seleccionar_fila(self, fila, _):
        self.input_id.setText(self.tabla.item(fila, 0).text())

        tipo_pago = self.tabla.item(fila, 1).text()
        index_pago = self.combo_pago.findText(tipo_pago)
        if index_pago != -1:
            self.combo_pago.setCurrentIndex(index_pago)

        id_venta = self.tabla.item(fila, 2).text()
        for i in range(self.combo_ventas.count()):
            if str(self.combo_ventas.itemData(i)) == id_venta:
                self.combo_ventas.setCurrentIndex(i)
                break

    def limpiar_campos(self):
        self.input_id.clear()
        self.combo_pago.setCurrentIndex(0)
        self.combo_ventas.setCurrentIndex(0)

    def validar_campos(self):
        if not all([self.input_id.text()]):
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos.")
            return False
        return True

    def agregar_ticket(self):
        if not self.validar_campos():
            return
        
        id_ticket = self.input_id.text()
        id_modo_pago = self.combo_pago.currentData()
        id_ventas = self.combo_ventas.currentData()

        if self.controller.crear_ticket(id_ticket, id_modo_pago, id_ventas):
            QMessageBox.information(self, "Éxito", "Ticket agregado correctamente")
            self.cargar_datos()
            self.limpiar_campos()

    def actualizar_ticket(self):
        if not self.validar_campos():
            return
        
        id_ticket = self.input_id.text()
        id_modo_pago = self.combo_pago.currentData()
        id_ventas = self.combo_ventas.currentData()

        if self.controller.actualizar_ticket(id_ticket, id_modo_pago, id_ventas):
            QMessageBox.information(self, "Éxito", "Ticket actualizado correctamente")
            self.cargar_datos()
            self.limpiar_campos()

    def eliminar_ticket(self):
        id_ticket = self.input_id.text()
        if not id_ticket:
            QMessageBox.warning(self, "Advertencia", "Ingrese el ID del ticket a eliminar.")
            return
        
        if self.controller.eliminar_ticket(id_ticket):
            QMessageBox.information(self, "Éxito", "Ticket eliminado correctamente")
            self.cargar_datos()
            self.limpiar_campos()

    def dibujar_texto(self, painter: QPainter, x: int, y: int, texto: str, font: QFont = None, bold: bool = False) -> int:
        current_font = painter.font()
        if font:
            current_font = font
        if bold:
            current_font.setBold(True)

        painter.setFont(current_font)
        font_metrics = QFontMetrics(current_font)
        painter.drawText(x, y, texto)
        return y + font_metrics.height() + 2

    def generar_impresion(self):
        id_ticket = self.input_id.text()

        if not id_ticket:
            QMessageBox.warning(self, "Advertencia", "Seleccione un ticket para imprimir.")
            return

        try:
            resultado = self.controller.obtener_detalles_impresion(id_ticket)

            if not resultado:
                QMessageBox.warning(self, "Advertencia", "No se encontraron detalles para este ticket.")
                return

            file_dialog = QFileDialog(self)
            file_dialog.setDefaultSuffix("pdf")
            file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
            file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
            file_dialog.setNameFilter("Archivos PDF (*.pdf)")

            if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
                file_path = file_dialog.selectedFiles()[0]
            else:
                return

            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_path)
            printer.setPageSize(QPageSize(QSizeF(40, 65), QPageSize.Unit.Millimeter))
            
            page_layout = QPageLayout(
                QPageSize(QSizeF(40, 65), QPageSize.Unit.Millimeter),
                QPageLayout.Orientation.Portrait,
                QMarginsF(5, 5, 5, 5)
            )
            printer.setPageLayout(page_layout)

            painter = QPainter()

            if not painter.begin(printer):
                QMessageBox.critical(self, "Error", "No se pudo iniciar la impresión.")
                return
            
            fuente = QFont("Courier New", 3)
            painter.setFont(fuente)
            fm = painter.fontMetrics()
            line_height = fm.height()

            x = 50
            y = 50

            def draw_line(text=""):
                nonlocal y
                painter.drawText(x, y, text)
                y += line_height

            # Encabezado
            est = resultado[0]
            draw_line("=" * 40)
            draw_line("Dulceria el conejo Feliz".center(40))

            # Logo
            logo_url = "https://dulceriaelconejofeliz.com/assets/logo-gqZwOJrA.png"
            try:
                with urlopen(logo_url) as response:
                    logo_data = response.read()
                    image = QImage()
                    image.loadFromData(logo_data)

                    if not image.isNull():
                        logo_width = 200
                        logo_height = int(image.height() * (logo_width / image.width()))
                        logo_scaled = image.scaled(logo_width, logo_height, Qt.AspectRatioMode.KeepAspectRatio)
                        page_rect = printer.pageRect(QPrinter.Unit.DevicePixel)
                        x_logo = int((page_rect.width() - logo_scaled.width()) / 2)
                        painter.drawImage(x_logo, y, logo_scaled)
                        y += logo_scaled.height() + 10
            except Exception as e:
                print(f"Error al cargar el logo: {e}")

            draw_line("Av 3a. Sur Pte 548, Centro, 29000 Tuxtla Gutiérrez, Chis.".center(40))
            draw_line("-" * 40)
            draw_line(f"Ticket: {est['id_ticket']}    Venta: {est['id_ventas']}")
            draw_line(f"Fecha: {str(est['fecha_venta'])}")
            draw_line(f"Modo de Pago: {est['modo_pago']}")
            draw_line("-" * 40)

            # Cliente y Cajero
            draw_line(f"Cliente: {est['nombre_cliente']}")
            draw_line(f"Tel. Cliente: {est['telefono_cliente']}")
            draw_line(f"Cajero: {est['nombre_usuario']}")
            draw_line(f"Tel. Cajero: {est['telefono_usuario']}")
            draw_line("=" * 40)

            # Tabla de artículos
            draw_line(f"{'Cód.':<6}{'Descripción':<12}{'Cant.':>6}{'P.U.':>9}{'Importe':>9}")
            draw_line("-" * 40)

            total = 0
            total_articulos = 0

            for item in resultado:
                cod = str(item['codigo_articulo'])[:6].ljust(6)
                descripcion = item['nombre_articulo'][:12].ljust(12)
                cantidad_val = float(item['cantidad'])
                cantidad = f"{cantidad_val:.2f}".rjust(6)
                precio_unitario = round(float(item['subtotal']) / cantidad_val, 2) if cantidad_val else 0.00
                precio = f"${precio_unitario:.2f}".rjust(9)
                importe = round(float(item['subtotal']), 2)
                subtotal = f"${importe:.2f}".rjust(9)

                draw_line(f"{cod}{descripcion}{cantidad}{precio}{subtotal}")
                total += importe
                total_articulos += cantidad_val

            # Totales
            iva = round(total * 0.16, 2)
            total_con_iva = round(total + iva, 2)

            draw_line("-" * 40)
            draw_line(f"Total Artículos: {total_articulos:.2f}".rjust(40))
            draw_line(f"{'Subtotal:':>28} ${total:.2f}")
            draw_line(f"{'IVA 16%:':>28}  ${iva:.2f}")
            draw_line(f"{'TOTAL:':>28}    ${total_con_iva:.2f}")
            draw_line("=" * 40)
            draw_line("¡Gracias por su compra!".center(40))
            draw_line("Vuelva pronto :)".center(40))
            draw_line("=" * 40)

            # Código QR
            qr_data = f"Ticket: {est['id_ticket']}\nVenta: {est['id_ventas']}\nTotal: ${total_con_iva:.2f}"
            qr = qrcode.make(qr_data)
            pil_image = qr.convert('RGB')
            qt_image = ImageQt(pil_image)
            qr_image = QImage(qt_image)

            qr_x = 10
            qr_y = y + 10
            painter.drawImage(qr_x, qr_y, qr_image)

            painter.end()
            QMessageBox.information(self, "Impresión", "El ticket se ha generado correctamente.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")