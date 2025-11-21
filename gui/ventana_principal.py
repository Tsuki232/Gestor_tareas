# /gui/ventana_principal.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QTabWidget
)
from PyQt5.QtCore import Qt

from estructuras.lista_doble import DoublyLinkedList, TaskNode
from estructuras.arbol_subtareas import ArbolSubtareas
from estructuras.grafo_tareas import GrafoTareas

from gui.componentes.lista_tareas_widget import ListaTareasWidget
from gui.ventana_subtareas import VentanaSubtareas
from gui.ventana_grafo import VentanaGrafo


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Proyectos - Estructuras No Lineales")
        self.setMinimumSize(900, 600)

        # estructuras
        self.lista_tareas = DoublyLinkedList()
        self.grafo = GrafoTareas()
        self.arboles_subtareas = {}  # nombre_tarea -> ArbolSubtareas

        # UI
        cont = QWidget()
        self.setCentralWidget(cont)
        layout = QVBoxLayout()
        cont.setLayout(layout)

        # header
        from PyQt5.QtWidgets import QLabel
        header = QHBoxLayout()
        title = QLabel("Gestor de Proyectos")
        title.setObjectName("appTitle")
        header.addWidget(title)
        header.addStretch(1)
        layout.addLayout(header)

        self.widget_lista = ListaTareasWidget(self.lista_tareas)
        layout.addWidget(self.widget_lista)

        # area de pestañas para abrir vistas principales en tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(lambda idx: self.tab_widget.removeTab(idx))
        layout.addWidget(self.tab_widget)

        botones = QHBoxLayout()
        btn_add = QPushButton("Agregar tarea")
        btn_del = QPushButton("Eliminar tarea")
        btn_open_sub = QPushButton("Abrir subtareas")
        btn_open_grafo = QPushButton("Abrir dependencias")
        # estilos
        btn_add.setObjectName("primary")
        btn_del.setObjectName("danger")
        btn_open_sub.setObjectName("primary")
        btn_open_grafo.setObjectName("primary")
        botones.addWidget(btn_add)
        botones.addWidget(btn_del)
        botones.addWidget(btn_open_sub)
        botones.addWidget(btn_open_grafo)
        layout.addLayout(botones)

        # conexiones
        btn_add.clicked.connect(self.agregar_tarea)
        btn_del.clicked.connect(self.eliminar_tarea)
        btn_open_sub.clicked.connect(self.abrir_subtareas)
        btn_open_grafo.clicked.connect(self.abrir_grafo)

        # conectar señales del widget lista (opcional)
        self.widget_lista.tareaDobleClick.connect(lambda nombre: self.abrir_subtareas_por_nombre(nombre))

    def agregar_tarea(self):
        # Abrir diálogo independiente para crear la tarea
        from gui.ventana_agregar_tarea import VentanaAgregarTarea
        dlg = VentanaAgregarTarea(parent=self)
        if dlg.exec_() != dlg.Accepted:
            return
        nombre = dlg.get_nombre()
        if not nombre:
            return
        nodo = TaskNode(nombre)
        self.lista_tareas.append(nodo)
        # crear árbol de subtareas y registrar en grafo
        arbol = ArbolSubtareas()
        nodo.subtareas_tree = arbol
        self.arboles_subtareas[nombre] = arbol
        self.grafo.agregar_tarea(nombre)
        self.widget_lista.actualizar()

    def eliminar_tarea(self):
        nombre = self.widget_lista.obtener_tarea_seleccionada()
        if not nombre:
            QMessageBox.warning(self, "Error", "Seleccione una tarea.")
            return
        # confirmar
        if QMessageBox.question(self, "Confirmar", f"Eliminar '{nombre}'?", QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
            return
        # eliminar de lista
        eliminado = self.lista_tareas.eliminar_por_nombre(nombre)
        # eliminar árbol
        self.arboles_subtareas.pop(nombre, None)
        # eliminar del grafo (nodos y aristas)
        if nombre in self.grafo.tareas:
            self.grafo.tareas.remove(nombre)
            self.grafo.adyacencia.pop(nombre, None)
            for t in list(self.grafo.adyacencia.keys()):
                self.grafo.adyacencia[t].discard(nombre)
        self.widget_lista.actualizar()

    def abrir_subtareas(self):
        nombre = self.widget_lista.obtener_tarea_seleccionada()
        if not nombre:
            QMessageBox.warning(self, "Error", "Seleccione una tarea.")
            return
        self.abrir_subtareas_por_nombre(nombre)

    def abrir_subtareas_por_nombre(self, nombre: str):
        arbol = self.arboles_subtareas.get(nombre)
        if arbol is None:
            arbol = ArbolSubtareas()
            self.arboles_subtareas[nombre] = arbol
        # Abrir en una pestaña: si ya existe la pestaña, activarla
        ventana = VentanaSubtareas(nombre, arbol, parent=self, on_close=self._close_tab_for_widget)
        # buscar si ya existe
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if isinstance(widget, VentanaSubtareas) and getattr(widget, 'tarea_nombre', None) == nombre:
                self.tab_widget.setCurrentIndex(i)
                return
        self.tab_widget.addTab(ventana, f"Subtareas: {nombre}")
        self.tab_widget.setCurrentWidget(ventana)

    def abrir_grafo(self):
        # Abrir grafo en una pestaña
        ventana = VentanaGrafo(self.grafo, parent=self, on_close=self._close_tab_for_widget)
        # si ya hay un grafo abierto (único), activar
        for i in range(self.tab_widget.count()):
            if isinstance(self.tab_widget.widget(i), VentanaGrafo):
                self.tab_widget.setCurrentIndex(i)
                return
        self.tab_widget.addTab(ventana, "Dependencias (Grafo)")
        self.tab_widget.setCurrentWidget(ventana)

    def _close_tab_for_widget(self, widget):
        # buscar índice de widget en tabs y remover
        for i in range(self.tab_widget.count()):
            if self.tab_widget.widget(i) is widget:
                self.tab_widget.removeTab(i)
                return
