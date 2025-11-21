# /gui/ventana_grafo.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QListWidgetItem, QInputDialog, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt

from estructuras.grafo_tareas import GrafoTareas
from gui.componentes.grafo_widget import GrafoWidget


class VentanaGrafo(QWidget):
    def __init__(self, grafo: GrafoTareas, parent=None, on_close=None):
        super().__init__(parent)
        if not isinstance(grafo, GrafoTareas):
            raise TypeError("VentanaGrafo espera una instancia de GrafoTareas")
        self.grafo = grafo
        self._on_close_callback = on_close
        self.setWindowTitle("Dependencias entre Tareas (Grafo)")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # header con volver
        header = QHBoxLayout()
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setObjectName("secondary")
        header.addWidget(self.btn_volver)
        header.addStretch(1)
        header.addWidget(QLabel("Dependencias (Grafo):"))
        header.addStretch(2)
        layout.addLayout(header)

        self.widget_grafo = GrafoWidget(self.grafo)
        layout.addWidget(self.widget_grafo)

        from PyQt5.QtWidgets import QGridLayout
        controles = QGridLayout()
        botones = [
            ("Agregar dependencia", "add"),
            ("Eliminar dependencia", "remove"),
            ("Refrescar", "refresh"),
            ("BFS desde...", "bfs"),
            ("DFS desde...", "dfs"),
            ("Orden topológico", "topo"),
            ("Detectar ciclos", "ciclos"),
            ("Tareas disponibles", "disp"),
        ]
        self._bot_refs = {}
        cols = 3
        for idx, (txt, key) in enumerate(botones):
            btn = QPushButton(txt)
            btn.setObjectName("primary")
            r = idx // cols
            c = idx % cols
            controles.addWidget(btn, r, c)
            self._bot_refs[key] = btn
        layout.addLayout(controles)

        self.btn_volver.clicked.connect(self._on_volver)
        self._bot_refs["add"].clicked.connect(self.agregar_dependencia)
        self._bot_refs["remove"].clicked.connect(self.eliminar_dependencia)
        self._bot_refs["refresh"].clicked.connect(self.refrescar)
        self._bot_refs["bfs"].clicked.connect(self.bfs_desde)
        self._bot_refs["dfs"].clicked.connect(self.dfs_desde)
        self._bot_refs["topo"].clicked.connect(self.mostrar_topologico)
        self._bot_refs["ciclos"].clicked.connect(self.mostrar_ciclos)
        self._bot_refs["disp"].clicked.connect(self.mostrar_disponibles)

    def _on_volver(self):
        """Handler para el botón Volver: cierra esta ventana."""
        cb = getattr(self, '_on_close_callback', None)
        if cb is not None and callable(cb):
            try:
                cb(self)
                return
            except Exception:
                pass
        self.close()

    def refrescar(self):
        self.widget_grafo.actualizar()

    def _eleccion_de_tarea(self, titulo: str, label: str):
        opciones = sorted(list(self.grafo.tareas))
        if not opciones:
            QMessageBox.warning(self, "No hay tareas", "No hay tareas registradas en el grafo.")
            return None
        item, ok = QInputDialog.getItem(self, titulo, label, opciones, 0, False)
        if not ok or not item:
            return None
        return item

    def agregar_dependencia(self):
        if not self.grafo.tareas:
            QMessageBox.warning(self, "Error", "No hay tareas en el grafo.")
            return
        from gui.ventana_agregar_dependencia import VentanaAgregarDependencia
        dlg = VentanaAgregarDependencia(self.grafo, parent=self)
        if dlg.exec_() != dlg.Accepted:
            return
        a, b = dlg.get_data()
        if not a or not b or a == b:
            QMessageBox.warning(self, "Error", "Selecciona dos tareas distintas.")
            return
        self.grafo.agregar_dependencia(a, b)
        QMessageBox.information(self, "Listo", f"{a} → {b}")
        self.refrescar()

    def eliminar_dependencia(self):
        a = self._eleccion_de_tarea("Origen", "Tarea A (origen):")
        if a is None:
            return
        vecinos = sorted(self.grafo.adyacencia.get(a, []))
        if not vecinos:
            QMessageBox.information(self, "Info", f"{a} no tiene dependencias salientes.")
            return
        b, ok = QInputDialog.getItem(self, "Destino", "Tarea B (destino):", vecinos, 0, False)
        if not ok or not b:
            return
        self.grafo.eliminar_dependencia(a, b)
        QMessageBox.information(self, "Listo", f"Eliminada {a} → {b}")
        self.refrescar()

    def bfs_desde(self):
        inicio = self._eleccion_de_tarea("BFS", "Nodo inicial:")
        if inicio is None:
            return
        rec = self.grafo.bfs(inicio)
        QMessageBox.information(self, f"BFS desde {inicio}", " → ".join(rec))

    def dfs_desde(self):
        inicio = self._eleccion_de_tarea("DFS", "Nodo inicial:")
        if inicio is None:
            return
        rec = self.grafo.dfs(inicio)
        QMessageBox.information(self, f"DFS desde {inicio}", " → ".join(rec))

    def mostrar_topologico(self):
        orden = self.grafo.orden_topologico()
        if not orden:
            QMessageBox.warning(self, "Topológico", "No se pudo obtener (posible ciclo).")
            return
        QMessageBox.information(self, "Orden topológico", " → ".join(orden))

    def mostrar_ciclos(self):
        tiene = self.grafo.tiene_ciclos()
        if tiene:
            QMessageBox.warning(self, "Ciclos", "Se detectó al menos un ciclo.")
        else:
            QMessageBox.information(self, "Ciclos", "No se detectaron ciclos.")

    def mostrar_disponibles(self):
        disp = self.grafo.tareas_disponibles()
        if not disp:
            QMessageBox.information(self, "Disponibles", "(Ninguna)")
            return
        QMessageBox.information(self, "Disponibles", " → ".join(sorted(disp)))
