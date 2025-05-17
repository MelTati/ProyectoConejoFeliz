import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
     QStackedWidget, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from views.ventas_view import VentanaVentas
from views.cliente_view import ClienteView
from views.articulo_view import VentanaArticulos
from views.usuarios_view import UsuariosView
from views.ticket_view import TicketView
from views.proveedor_view import VentanaProveedor
from views.compras_view import VentanaCompras
from views.marcas_view import MarcasView
from views.categorias_view import CategoriaView

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #FFF8FC;")  # Fondo general claro con un toque rosado


        self.stacked_widget = QStackedWidget()

        # Crear instancias de las ventanas
        self.ventas = VentanaVentas()
        self.ticket = TicketView()
        self.clientes = ClienteView()
        self.articulos = VentanaArticulos()
        self.usuarios = UsuariosView()
        self.compras = VentanaCompras()
        self.proveedores = VentanaProveedor()
        self.marcas = MarcasView()
        self.categorias =CategoriaView()

        # Agregar widgets al stack
        self.stacked_widget.addWidget(self.ventas)
        self.stacked_widget.addWidget(self.ticket)
        self.stacked_widget.addWidget(self.clientes)
        self.stacked_widget.addWidget(self.articulos)
        self.stacked_widget.addWidget(self.usuarios)
        self.stacked_widget.addWidget(self.compras)
        self.stacked_widget.addWidget(self.proveedores)
        self.stacked_widget.addWidget(self.marcas)
        self.stacked_widget.addWidget(self.categorias)
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()

        # Sidebar moderno claro
        sidebar = QVBoxLayout()
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(220)
        sidebar_widget.setStyleSheet("""
             background-color: #6F2DA8;
             border-right: 1px solid #5A189A;
        """)

        botones = [
            ("Ventas", lambda: self.stacked_widget.setCurrentIndex(0)),
             ("Tickets", lambda: self.stacked_widget.setCurrentIndex(1)),
            ("Clientes", lambda: self.stacked_widget.setCurrentIndex(2)),
            ("Artículos", lambda: self.stacked_widget.setCurrentIndex(3)),
            ("Usuarios", lambda: self.stacked_widget.setCurrentIndex(4)),
            ("Compras", lambda: self.stacked_widget.setCurrentIndex(5)),
            ("Proveedor", lambda: self.stacked_widget.setCurrentIndex(6)),
            ("Marcas", lambda: self.stacked_widget.setCurrentIndex(7)),
            ("Categorias", lambda: self.stacked_widget.setCurrentIndex(8))
        ]

        label_title = QLabel("Menú Principal")
        label_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        label_title.setStyleSheet("color: #FFD700; padding: 20px 10px;")
        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar.addWidget(label_title)

        for texto, accion in botones:
            btn = QPushButton(texto)
            btn.setFont(QFont("Segoe UI", 11))
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                 QPushButton {
                background-color: #FFD700;
                color: #6F2DA8;
                border: 1px solid #E5C100;
                border-radius: 10px;
                margin: 6px 16px;
            }
            QPushButton:hover {
                background-color: #FFF176;
                border-color: #FDD835;
            }
            """)
            btn.clicked.connect(accion)
            sidebar.addWidget(btn)

        sidebar.addStretch()
        sidebar_widget.setLayout(sidebar)

        # Área de contenido
        content_layout = QVBoxLayout()
        content_widget = QWidget()

        header = QLabel("Bienvenido al Sistema de Gestión")
        header.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #6F2DA8; padding: 20px; background-color: #FFD700; border-radius: 10px;")
        content_layout.addWidget(header)
        content_layout.addWidget(self.stacked_widget)
        content_widget.setLayout(content_layout)

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)
