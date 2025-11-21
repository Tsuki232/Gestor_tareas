# /estructuras/grafo_tareas.py
from __future__ import annotations
from typing import Dict, List, Set
from collections import deque


class GrafoTareas:
    def __init__(self):
        self.adyacencia: Dict[str, Set[str]] = {}
        self.tareas: Set[str] = set()

    def agregar_tarea(self, nombre: str):
        if nombre not in self.tareas:
            self.tareas.add(nombre)
            self.adyacencia[nombre] = set()

    def agregar_dependencia(self, tarea_a: str, tarea_b: str):
        if tarea_a not in self.tareas:
            self.agregar_tarea(tarea_a)
        if tarea_b not in self.tareas:
            self.agregar_tarea(tarea_b)
        self.adyacencia[tarea_a].add(tarea_b)

    def eliminar_dependencia(self, tarea_a: str, tarea_b: str):
        if tarea_a in self.adyacencia:
            self.adyacencia[tarea_a].discard(tarea_b)

    def obtener_dependencias(self, nombre: str) -> List[str]:
        return list(self.adyacencia.get(nombre, []))

    def bfs(self, inicio: str) -> List[str]:
        visitados = []
        cola = deque([inicio])
        vistos = set()
        while cola:
            nodo = cola.popleft()
            if nodo not in vistos:
                visitados.append(nodo)
                vistos.add(nodo)
                for vecino in self.adyacencia.get(nodo, []):
                    cola.append(vecino)
        return visitados

    def dfs(self, inicio: str) -> List[str]:
        resultado = []
        visitados = set()
        def _dfs(nodo):
            if nodo in visitados:
                return
            visitados.add(nodo)
            resultado.append(nodo)
            for vecino in self.adyacencia.get(nodo, []):
                _dfs(vecino)
        _dfs(inicio)
        return resultado

    def tiene_ciclos(self) -> bool:
        estado = {t: "blanco" for t in self.tareas}
        def _dfs(n):
            if estado[n] == "gris":
                return True
            if estado[n] == "negro":
                return False
            estado[n] = "gris"
            for vecino in self.adyacencia.get(n, []):
                if _dfs(vecino):
                    return True
            estado[n] = "negro"
            return False
        for t in list(self.tareas):
            if estado[t] == "blanco":
                if _dfs(t):
                    return True
        return False

    def orden_topologico(self) -> List[str]:
        indegree = {t: 0 for t in self.tareas}
        for a in self.adyacencia:
            for b in self.adyacencia[a]:
                indegree[b] += 1
        cola = deque([t for t in self.tareas if indegree[t] == 0])
        resultado = []
        while cola:
            nodo = cola.popleft()
            resultado.append(nodo)
            for vecino in self.adyacencia[nodo]:
                indegree[vecino] -= 1
                if indegree[vecino] == 0:
                    cola.append(vecino)
        if len(resultado) != len(self.tareas):
            return []
        return resultado

    def tareas_disponibles(self) -> List[str]:
        indegree = {t: 0 for t in self.tareas}
        for a in self.adyacencia:
            for b in self.adyacencia[a]:
                indegree[b] += 1
        return [t for t, deg in indegree.items() if deg == 0]
