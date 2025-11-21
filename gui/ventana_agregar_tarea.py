from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt


class VentanaAgregarTarea(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar tarea")
        self.setMinimumSize(420, 150)
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Nombre de la nueva tarea:"))
        self.input_nombre = QLineEdit()
        layout.addWidget(self.input_nombre)

        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Crear")
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_ok.setDefault(True)
        btns.addStretch(1)
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def get_nombre(self):
        return self.input_nombre.text().strip()
