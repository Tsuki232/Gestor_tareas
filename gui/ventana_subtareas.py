# /gui/ventana_subtareas.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QMessageBox, QInputDialog, QSizePolicy
)
from PyQt5.QtCore import Qt

from estructuras.arbol_subtareas import ArbolSubtareas
from gui.componentes.arbol_widget import ArbolWidget


class VentanaSubtareas(QWidget):
    def __init__(self, tarea_nombre: str, arbol: ArbolSubtareas, parent=None, on_close=None):
        super().__init__(parent)
        self._on_close_callback = on_close
        self.tarea_nombre = tarea_nombre
        self.arbol = arbol
        self.setWindowTitle(f"Subtareas de: {self.tarea_nombre}")
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.lbl_info = QLabel(f"Subtareas de: {self.tarea_nombre}")
        self.lbl_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # cabecera con botón volver y título
        header_layout = QHBoxLayout()
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setObjectName("secondary")
        header_layout.addWidget(self.btn_volver)
        header_layout.addStretch(1)
        header_layout.addWidget(self.lbl_info)
        header_layout.addStretch(2)
        layout.addLayout(header_layout)

        # área visual del árbol
        self.widget_arbol = ArbolWidget(self.arbol)
        self.widget_arbol.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.widget_arbol)

        # acciones (etiquetas más amigables)
        from PyQt5.QtWidgets import QGridLayout
        botones_layout = QGridLayout()
        botones = [
            ("Agregar subtarea principal", "agregar_raiz"),
            ("Agregar subtarea secundaria (izq)", "agregar_izq"),
            ("Agregar subtarea secundaria (der)", "agregar_der"),
            ("Eliminar subtarea", "eliminar"),
            ("Marcar como completada", "marcar"),
            ("Recorrido Preorder", "pre"),
            ("Recorrido Inorder", "in"),
            ("Recorrido Postorder", "post"),
        ]

        self._botones_refs = {}
        cols = 3
        for idx, (text, key) in enumerate(botones):
            btn = QPushButton(text)
            btn.setObjectName("primary")
            r = idx // cols
            c = idx % cols
            botones_layout.addWidget(btn, r, c)
            self._botones_refs[key] = btn

        layout.addLayout(botones_layout)

        # conexiones
        self.btn_volver.clicked.connect(self._on_volver)
        # conectar botones desde refs
        self._botones_refs["agregar_raiz"].clicked.connect(self.crear_raiz)
        self._botones_refs["agregar_izq"].clicked.connect(lambda: self.agregar_subtarea("izquierda"))
        self._botones_refs["agregar_der"].clicked.connect(lambda: self.agregar_subtarea("derecha"))
        self._botones_refs["eliminar"].clicked.connect(self.eliminar_subtarea)
        self._botones_refs["marcar"].clicked.connect(self.marcar_subtarea)
        self._botones_refs["pre"].clicked.connect(lambda: self.mostrar_recorrido("pre"))
        self._botones_refs["in"].clicked.connect(lambda: self.mostrar_recorrido("in"))
        self._botones_refs["post"].clicked.connect(lambda: self.mostrar_recorrido("post"))

    def crear_raiz(self):
        # Usar diálogo especializado para crear la subtarea raíz
        if self.arbol.root is not None:
            QMessageBox.information(self, "Info", "Ya existe una subtarea principal.")
            return
        from gui.ventana_agregar_subtarea import VentanaAgregarSubtarea
        dlg = VentanaAgregarSubtarea(self.arbol, modo_root=True, parent=self)
        if dlg.exec_() != dlg.Accepted:
            return
        data = dlg.get_data()
        nombre = data.get("nombre")
        if not nombre:
            return
        self.arbol.insertar_raiz(nombre)
        self.widget_arbol.actualizar()

    def _on_volver(self):
        """Handler para el botón Volver: cierra esta ventana."""
        # Si se pasó un callback, usarlo para que el padre cierre la pestaña
        cb = getattr(self, '_on_close_callback', None)
        if callable(cb):
            try:
                cb(self)
                return
            except Exception:
                pass
        # Fallback: cerrar la ventana si no hay callback
        self.close()

    def _elegir_nodo(self, prompt="Elige subtarea (nombre exacto)"):
        # pide al usuario el nombre de la subtarea padre (lista de opciones)
        nombres = self.arbol.preorder()
        if not nombres:
            QMessageBox.warning(self, "Error", "El árbol está vacío.")
            return None
        item, ok = QInputDialog.getItem(self, "Seleccionar nodo", prompt, nombres, 0, False)
        if not ok or not item:
            return None
        return item

    def agregar_subtarea(self, lado: str):
        # Abrir diálogo que permite seleccionar padre, lado y nombre
        if self.arbol.root is None:
            QMessageBox.information(self, "Info", "No existe una subtarea principal. Usa 'Agregar subtarea principal'.")
            return
        from gui.ventana_agregar_subtarea import VentanaAgregarSubtarea
        dlg = VentanaAgregarSubtarea(self.arbol, modo_root=False, parent=self)
        if dlg.exec_() != dlg.Accepted:
            return
        data = dlg.get_data()
        nombre = data.get("nombre") or ""
        padre = data.get("padre") or ""
        lado = data.get("lado") or "izquierda"
        if not nombre or not padre:
            return
        try:
            self.arbol.insertar_subtarea(padre, nombre, lado=lado)
            self.widget_arbol.actualizar()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def eliminar_subtarea(self):
        nombre = self._elegir_nodo("Seleccione la subtarea a eliminar:")
        if nombre is None:
            return
        if QMessageBox.question(self, "Confirmar", f"Eliminar '{nombre}'?", QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
            return
        self.arbol.eliminar_subtarea(nombre)
        self.widget_arbol.actualizar()

    def marcar_subtarea(self):
        nombre = self._elegir_nodo("Seleccione la subtarea a marcar completada:")
        if nombre is None:
            return
        try:
            exito = self.arbol.marcar_completada(nombre)
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
            return
        if not exito:
            QMessageBox.warning(self, "No puede completarse", "Debe completar primero sus dependencias.")
            return
        self.widget_arbol.actualizar()

    def mostrar_recorrido(self, tipo: str):
        if self.arbol.root is None:
            QMessageBox.information(self, "Recorrido", "El árbol está vacío.")
            return
        if tipo == "pre":
            datos = self.arbol.preorder()
            titulo = "Preorder"
        elif tipo == "in":
            datos = self.arbol.inorder()
            titulo = "Inorder"
        else:
            datos = self.arbol.postorder()
            titulo = "Postorder"
        QMessageBox.information(self, titulo, " → ".join(datos))
