# /gui/componentes/arbol_widget.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont

from estructuras.arbol_subtareas import ArbolSubtareas, SubtareaNode


class ArbolWidget(QWidget):
    def __init__(self, arbol: ArbolSubtareas = None, parent=None): # type: ignore
        super().__init__(parent)
        self.arbol = arbol if arbol is not None else ArbolSubtareas()
        self.setMinimumSize(600, 300)
        self.radio_nodo = 28
        self.dist_x = 80
        self.dist_y = 80

    def set_arbol(self, arbol: ArbolSubtareas):
        self.arbol = arbol
        self.update()

    def actualizar(self):
        self.update()

    def paintEvent(self, event):
        if not self.arbol or not self.arbol.root:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self._dibujar_nodo(painter, self.arbol.root, x=self.width() // 2, y=40, nivel=1)

    def _dibujar_nodo(self, painter: QPainter, nodo: SubtareaNode, x: int, y: int, nivel: int):
        if nodo is None:
            return
        # hijos
        if nodo.izquierda:
            x_izq = x - self.dist_x * nivel
            y_izq = y + self.dist_y
            painter.setPen(QPen(Qt.black, 2)) # type: ignore
            painter.drawLine(x, y, x_izq, y_izq)
            self._dibujar_nodo(painter, nodo.izquierda, x_izq, y_izq, nivel + 1)
        if nodo.derecha:
            x_der = x + self.dist_x * nivel
            y_der = y + self.dist_y
            painter.setPen(QPen(Qt.black, 2)) # type: ignore
            painter.drawLine(x, y, x_der, y_der)
            self._dibujar_nodo(painter, nodo.derecha, x_der, y_der, nivel + 1)
        # color por estado
        color = QColor(180, 230, 180) if nodo.estado == "completada" else QColor(250, 250, 210)
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.darkBlue, 2)) # type: ignore
        painter.drawEllipse(x - self.radio_nodo, y - self.radio_nodo, self.radio_nodo * 2, self.radio_nodo * 2)
        painter.setFont(QFont("Arial", 9))
        painter.setPen(Qt.black) # type: ignore
        texto = nodo.nombre
        painter.drawText(x - self.radio_nodo, y - 7, self.radio_nodo * 2, self.radio_nodo * 2, Qt.AlignmentFlag.AlignCenter, texto)
