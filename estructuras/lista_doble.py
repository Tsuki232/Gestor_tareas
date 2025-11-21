# /estructuras/lista_doble.py
from __future__ import annotations
from typing import Optional, List, Any, Iterable


class TaskNode:
    __slots__ = ("nombre", "descripcion", "estado", "prioridad", "fecha",
                 "prev", "next", "subtareas_tree", "graph_id")

    def __init__(self,
                 nombre: str,
                 descripcion: str = "",
                 estado: str = "pendiente",
                 prioridad: int = 5,
                 fecha: Optional[str] = None):
        self.nombre: str = nombre
        self.descripcion: str = descripcion
        self.estado: str = estado
        self.prioridad: int = prioridad
        self.fecha: Optional[str] = fecha

        # enlaces de la lista doble
        self.prev: Optional[TaskNode] = None
        self.next: Optional[TaskNode] = None

        # referencias a otras estructuras (rellenadas por la capa superior)
        self.subtareas_tree: Optional[Any] = None  # instancia de ArbolSubtareas
        self.graph_id: Optional[Any] = None  # id del nodo en grafo de dependencias

    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "prioridad": self.prioridad,
            "fecha": self.fecha,
            "has_tree": self.subtareas_tree is not None,
            "graph_id": self.graph_id,
        }

    def __repr__(self) -> str:
        return f"<TaskNode {self.nombre} ({self.estado}) p={self.prioridad}>"


class DoublyLinkedList:
    def __init__(self):
        self.head: Optional[TaskNode] = None
        self.tail: Optional[TaskNode] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def append(self, node: TaskNode) -> TaskNode:
        if not isinstance(node, TaskNode):
            raise TypeError("append espera un TaskNode")
        if self.is_empty():
            self.head = self.tail = node
            node.prev = node.next = None
        else:
            assert self.tail is not None
            self.tail.next = node
            node.prev = self.tail
            node.next = None
            self.tail = node
        self._size += 1
        return node

    def prepend(self, node: TaskNode) -> TaskNode:
        if not isinstance(node, TaskNode):
            raise TypeError("prepend espera un TaskNode")
        if self.is_empty():
            self.head = self.tail = node
            node.prev = node.next = None
        else:
            assert self.head is not None
            self.head.prev = node
            node.next = self.head
            node.prev = None
            self.head = node
        self._size += 1
        return node

    def insert_after(self, target: TaskNode, new_node: TaskNode) -> TaskNode:
        if target is None:
            return self.append(new_node)
        if not isinstance(new_node, TaskNode):
            raise TypeError("insert_after espera un TaskNode")
        next_node = target.next
        target.next = new_node
        new_node.prev = target
        new_node.next = next_node
        if next_node:
            next_node.prev = new_node
        else:
            self.tail = new_node
        self._size += 1
        return new_node

    def remove(self, node: TaskNode) -> TaskNode:
        if self.is_empty():
            raise ValueError("La lista está vacía")
        if not isinstance(node, TaskNode):
            raise TypeError("remove espera un TaskNode")
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = node.next = None
        self._size -= 1
        return node

    def find(self, predicate) -> Optional[TaskNode]:
        cur = self.head
        while cur:
            if predicate(cur):
                return cur
            cur = cur.next
        return None

    def find_by_name(self, nombre: str) -> Optional[TaskNode]:
        return self.find(lambda n: n.nombre == nombre)

    def to_list(self) -> List[dict]:
        result = []
        cur = self.head
        while cur:
            result.append(cur.to_dict())
            cur = cur.next
        return result

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur
            cur = cur.next

    def clear(self):
        cur = self.head
        while cur:
            nxt = cur.next
            cur.prev = cur.next = None
            cur.subtareas_tree = None
            cur.graph_id = None
            cur = nxt
        self.head = self.tail = None
        self._size = 0

    # helper methods by name to be used in GUI convenience
    def agregar_al_final(self, nombre: str, descripcion: str = "", prioridad: int = 5) -> TaskNode:
        node = TaskNode(nombre, descripcion=descripcion, prioridad=prioridad)
        return self.append(node)

    def eliminar_por_nombre(self, nombre: str) -> bool:
        nodo = self.find_by_name(nombre)
        if nodo:
            self.remove(nodo)
            return True
        return False

    def serialize(self) -> List[dict]:
        return self.to_list()

    @classmethod
    def from_iterable(cls, items: Iterable[dict]) -> "DoublyLinkedList":
        lst = cls()
        for itm in items:
            node = TaskNode(
                nombre=itm.get("nombre", ""),
                descripcion=itm.get("descripcion", ""),
                estado=itm.get("estado", "pendiente"),
                prioridad=itm.get("prioridad", 5),
                fecha=itm.get("fecha")
            )
            lst.append(node)
        return lst
