from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox
from PyQt5.QtCore import Qt


class VentanaAgregarDependencia(QDialog):
    def __init__(self, grafo, parent=None):
        super().__init__(parent)
        self.grafo = grafo
        self.setWindowTitle("Agregar dependencia")
        self.setMinimumSize(520, 180)
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Tarea origen (A):"))
        self.cmb_a = QComboBox()
        layout.addWidget(self.cmb_a)

        layout.addWidget(QLabel("Tarea destino (B):"))
        self.cmb_b = QComboBox()
        layout.addWidget(self.cmb_b)

        opciones = sorted(list(self.grafo.tareas))
        self.cmb_a.addItems(opciones)
        self.cmb_b.addItems(opciones)

        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Agregar")
        self.btn_cancel = QPushButton("Cancelar")
        btns.addStretch(1)
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def get_data(self):
        return (self.cmb_a.currentText(), self.cmb_b.currentText())
