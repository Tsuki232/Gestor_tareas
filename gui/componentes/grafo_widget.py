# /gui/componentes/grafo_widget.py
import networkx as nx
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from estructuras.grafo_tareas import GrafoTareas


class GrafoWidget(QWidget):
    def __init__(self, grafo: GrafoTareas, parent=None):
        super().__init__(parent)
        if not isinstance(grafo, GrafoTareas):
            raise TypeError("GrafoWidget requiere una instancia de GrafoTareas.")
        self.grafo = grafo
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.canvas)
        self.dibujar()

    def set_grafo(self, grafo: GrafoTareas):
        self.grafo = grafo
        self.dibujar()

    def actualizar(self):
        self.dibujar()

    def dibujar(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        G = nx.DiGraph()
        for tarea in self.grafo.tareas:
            G.add_node(tarea)
        for origen, destinos in self.grafo.adyacencia.items():
            for destino in destinos:
                G.add_edge(origen, destino)
        if len(G.nodes) == 0:
            ax.text(0.5, 0.5, "Grafo vacío", horizontalalignment='center', verticalalignment='center')
            ax.set_axis_off()
            self.canvas.draw()
            return
        pos = nx.spring_layout(G, seed=42)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=900, node_color="lightblue", edgecolors="black")
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=9)
        nx.draw_networkx_edges(G, pos, ax=ax, width=2, arrows=True, arrowstyle="-|>", arrowsize=14)
        ax.set_axis_off()
        self.canvas.draw()
