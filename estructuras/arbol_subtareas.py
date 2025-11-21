# /estructuras/arbol_subtareas.py
from __future__ import annotations
from typing import Optional, List


class SubtareaNode:
    __slots__ = ("nombre", "descripcion", "estado", "izquierda", "derecha")

    def __init__(self, nombre: str, descripcion: str = "", estado: str = "pendiente"):
        self.nombre: str = nombre
        self.descripcion: str = descripcion
        self.estado: str = estado  # "pendiente" | "completada"
        self.izquierda: Optional[SubtareaNode] = None
        self.derecha: Optional[SubtareaNode] = None

    def __repr__(self):
        return f"<SubtareaNode {self.nombre} ({self.estado})>"


class ArbolSubtareas:
    def __init__(self):
        self.root: Optional[SubtareaNode] = None

    def insertar_raiz(self, nombre: str, descripcion: str = "") -> SubtareaNode:
        if self.root is not None:
            raise ValueError("La raíz ya existe.")
        self.root = SubtareaNode(nombre, descripcion)
        return self.root

    def insertar_subtarea(self, parent_nombre: str, nombre: str, descripcion: str = "", lado: str = "izquierda") -> SubtareaNode:
        if self.root is None:
            raise ValueError("No existe raíz.")
        padre = self.buscar_por_nombre(parent_nombre)
        if padre is None:
            raise ValueError(f"No existe la subtarea padre '{parent_nombre}'.")
        nuevo = SubtareaNode(nombre, descripcion)
        if lado == "izquierda":
            if padre.izquierda is not None:
                raise ValueError(f"'{parent_nombre}' ya tiene dependencia izquierda.")
            padre.izquierda = nuevo
        elif lado == "derecha":
            if padre.derecha is not None:
                raise ValueError(f"'{parent_nombre}' ya tiene dependencia derecha.")
            padre.derecha = nuevo
        else:
            raise ValueError("lado debe ser 'izquierda' o 'derecha'.")
        return nuevo

    def buscar_por_nombre(self, nombre: str) -> Optional[SubtareaNode]:
        def _buscar(nodo: Optional[SubtareaNode]) -> Optional[SubtareaNode]:
            if nodo is None:
                return None
            if nodo.nombre == nombre:
                return nodo
            return _buscar(nodo.izquierda) or _buscar(nodo.derecha)
        return _buscar(self.root)

    def puede_completarse(self, nodo: SubtareaNode) -> bool:
        if nodo.izquierda and nodo.izquierda.estado != "completada":
            return False
        if nodo.derecha and nodo.derecha.estado != "completada":
            return False
        return True

    def marcar_completada(self, nombre: str) -> bool:
        nodo = self.buscar_por_nombre(nombre)
        if nodo is None:
            raise ValueError(f"No existe la subtarea '{nombre}'.")
        if self.puede_completarse(nodo):
            nodo.estado = "completada"
            return True
        return False

    def eliminar_subtarea(self, nombre: str) -> bool:
        def _eliminar(nodo: Optional[SubtareaNode], nombre: str) -> Optional[SubtareaNode]:
            if nodo is None:
                return None
            if nodo.nombre == nombre:
                return None
            nodo.izquierda = _eliminar(nodo.izquierda, nombre)
            nodo.derecha = _eliminar(nodo.derecha, nombre)
            return nodo
        if self.root is None:
            return False
        if self.root.nombre == nombre:
            self.root = None
            return True
        antes = self.buscar_por_nombre(nombre)
        self.root = _eliminar(self.root, nombre)
        despues = self.buscar_por_nombre(nombre)
        return antes is not None and despues is None

    def preorder(self) -> List[str]:
        lista = []
        def _pre(n):
            if n:
                lista.append(n.nombre)
                _pre(n.izquierda)
                _pre(n.derecha)
        _pre(self.root)
        return lista

    def inorder(self) -> List[str]:
        lista = []
        def _in(n):
            if n:
                _in(n.izquierda)
                lista.append(n.nombre)
                _in(n.derecha)
        _in(self.root)
        return lista

    def postorder(self) -> List[str]:
        lista = []
        def _post(n):
            if n:
                _post(n.izquierda)
                _post(n.derecha)
                lista.append(n.nombre)
        _post(self.root)
        return lista
