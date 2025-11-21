from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt5.QtCore import Qt


class VentanaAgregarSubtarea(QDialog):
    def __init__(self, arbol, modo_root=False, parent=None):
        super().__init__(parent)
        self.arbol = arbol
        self.modo_root = modo_root
        self.setWindowTitle("Agregar subtarea")
        self.setMinimumSize(480, 200)
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout()
        self.setLayout(layout)

        if not modo_root:
            layout.addWidget(QLabel("Seleccionar subtarea padre:"))
            self.cmb_padre = QComboBox()
            nombres = self.arbol.preorder()
            self.cmb_padre.addItems(nombres)
            layout.addWidget(self.cmb_padre)

            layout.addWidget(QLabel("Lado:"))
            self.cmb_lado = QComboBox()
            self.cmb_lado.addItems(["izquierda", "derecha"])
            layout.addWidget(self.cmb_lado)
        else:
            layout.addWidget(QLabel("Crear subtarea raíz:"))

        layout.addWidget(QLabel("Nombre de la subtarea:"))
        self.input_nombre = QLineEdit()
        layout.addWidget(self.input_nombre)

        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Crear")
        self.btn_cancel = QPushButton("Cancelar")
        btns.addStretch(1)
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def get_data(self):
        nombre = self.input_nombre.text().strip()
        if self.modo_root:
            return {"nombre": nombre}
        padre = self.cmb_padre.currentText()
        lado = self.cmb_lado.currentText()
        return {"padre": padre, "lado": lado, "nombre": nombre}
