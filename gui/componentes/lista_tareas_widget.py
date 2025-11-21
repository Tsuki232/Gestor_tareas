# /gui/componentes/lista_tareas_widget.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import QSize
from PyQt5.QtCore import pyqtSignal

from estructuras.lista_doble import DoublyLinkedList


class ListaTareasWidget(QWidget):
    tareaSeleccionada = pyqtSignal(str)
    tareaDobleClick = pyqtSignal(str)
    listaActualizada = pyqtSignal()

    def __init__(self, lista_tareas: DoublyLinkedList, parent=None):
        super().__init__(parent)
        if not isinstance(lista_tareas, DoublyLinkedList):
            raise TypeError("ListaTareasWidget requiere una instancia de DoublyLinkedList.")
        self.lista = lista_tareas
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.lista_widget = QListWidget()
        # Mostrar como cuadrícula (icon mode) para permitir filas/columnas
        self.lista_widget.setViewMode(QListWidget.IconMode)
        self.lista_widget.setResizeMode(QListWidget.Adjust)
        self.lista_widget.setWrapping(True)
        self.lista_widget.setGridSize(QSize(220, 64))
        layout.addWidget(self.lista_widget)
        self.lista_widget.itemClicked.connect(self._emitir_seleccion)
        self.lista_widget.itemDoubleClicked.connect(self._emitir_doble_click)
        self.actualizar()

    def actualizar(self):
        self.lista_widget.clear()
        if self.lista.is_empty():
            self.lista_widget.addItem("<< No hay tareas >>")
            self.listaActualizada.emit()
            return
        cur = self.lista.head
        while cur:
            item = QListWidgetItem(cur.nombre)
            self.lista_widget.addItem(item)
            cur = cur.next
        self.listaActualizada.emit()

    from typing import Optional

    def obtener_tarea_seleccionada(self) -> Optional[str]:
        item = self.lista_widget.currentItem()
        return item.text() if item else None

    def seleccionar_tarea(self, nombre: str):
        for i in range(self.lista_widget.count()):
            item = self.lista_widget.item(i)
            if item is not None and item.text() == nombre:
                self.lista_widget.setCurrentRow(i)
                break

    def _emitir_seleccion(self, item):
        self.tareaSeleccionada.emit(item.text())

    def _emitir_doble_click(self, item):
        self.tareaDobleClick.emit(item.text())
