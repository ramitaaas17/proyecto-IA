"""
Módulo de visualización de grafos
Usa matplotlib y networkx para dibujar los grafos
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class VisualizadorGrafo:
    """
    Clase para visualizar grafos con matplotlib
    """
    def __init__(self, parent, colores):
        self.parent = parent
        self.colores = colores
        self.canvas = None
        self.fig = None
    
    def dibujar_grafo(self, G, camino_resaltado=None):
        """
        Dibuja el grafo en el canvas
        
        Args:
            G: grafo de NetworkX
            camino_resaltado: lista de nodos que forman el camino a resaltar
        """
        # Limpiar canvas anterior si existe
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        if self.fig:
            plt.close(self.fig)
        
        # Crear nueva figura
        self.fig, ax = plt.subplots(figsize=(9, 7), facecolor=self.colores['bg_light'])
        ax.set_facecolor(self.colores['bg_light'])
        
        # Layout del grafo (posición de los nodos)
        pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
        
        # Dibujar aristas normales
        nx.draw_networkx_edges(G, pos,
                              edge_color='#444444',
                              width=1.5,
                              alpha=0.5,
                              ax=ax)
        
        # Resaltar camino si existe
        if camino_resaltado and len(camino_resaltado) > 1:
            # Crear aristas del camino
            camino_edges = [(camino_resaltado[i], camino_resaltado[i+1])
                           for i in range(len(camino_resaltado)-1)]
            
            # Dibujar aristas del camino resaltadas
            nx.draw_networkx_edges(G, pos,
                                  edgelist=camino_edges,
                                  edge_color=self.colores['accent_orange'],
                                  width=4,
                                  alpha=0.9,
                                  ax=ax,
                                  arrows=True,
                                  arrowsize=20,
                                  arrowstyle='->')
        
        # Determinar colores de nodos
        node_colors = []
        for node in G.nodes():
            if camino_resaltado and len(camino_resaltado) > 0:
                if node == camino_resaltado[0]:
                    # Nodo inicial en verde
                    node_colors.append(self.colores['accent_green'])
                elif node == camino_resaltado[-1]:
                    # Nodo final en rojo
                    node_colors.append(self.colores['accent_red'])
                elif node in camino_resaltado:
                    # Nodos del camino en naranja
                    node_colors.append(self.colores['accent_orange'])
                else:
                    # Nodos normales
                    node_colors.append(self.colores['accent_blue'])
            else:
                # Todos los nodos azules si no hay camino
                node_colors.append(self.colores['accent_blue'])
        
        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos,
                              node_color=node_colors,
                              node_size=800,
                              alpha=0.9,
                              ax=ax,
                              edgecolors='white',
                              linewidths=2)
        
        # Etiquetas de nodos
        nx.draw_networkx_labels(G, pos,
                               font_size=9,
                               font_color='white',
                               font_weight='bold',
                               ax=ax)
        
        # Obtener pesos de las aristas
        edge_labels = nx.get_edge_attributes(G, 'weight')
        
        # Formatear pesos (mostrar solo 1 decimal si es necesario)
        edge_labels_formatted = {
            k: f"{v:.1f}" if v % 1 != 0 else f"{int(v)}"
            for k, v in edge_labels.items()
        }
        
        # Dibujar pesos de aristas
        nx.draw_networkx_edge_labels(G, pos,
                                     edge_labels=edge_labels_formatted,
                                     font_size=8,
                                     font_color=self.colores['text_primary'],
                                     bbox=dict(boxstyle='round,pad=0.3',
                                             facecolor=self.colores['bg_medium'],
                                             edgecolor='none',
                                             alpha=0.8),
                                     ax=ax)
        
        # Agregar leyenda si hay camino
        if camino_resaltado and len(camino_resaltado) > 1:
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor=self.colores['accent_green'], label='Inicio'),
                Patch(facecolor=self.colores['accent_orange'], label='Camino'),
                Patch(facecolor=self.colores['accent_red'], label='Objetivo'),
                Patch(facecolor=self.colores['accent_blue'], label='Otros nodos')
            ]
            ax.legend(handles=legend_elements,
                     loc='upper right',
                     facecolor=self.colores['bg_medium'],
                     edgecolor=self.colores['border'],
                     labelcolor=self.colores['text_primary'],
                     fontsize=9)
        
        # Quitar ejes
        ax.axis('off')
        ax.margins(0.1)
        
        # Ajustar layout
        plt.tight_layout()
        
        # Incrustar en tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def limpiar(self):
        """Limpia la visualización actual"""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        
        if self.fig:
            plt.close(self.fig)
            self.fig = None