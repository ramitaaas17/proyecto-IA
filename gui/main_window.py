"""
Ventana principal de la aplicación
Aquí se ensamblan todos los componentes de la interfaz
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import time
import networkx as nx

from config.styles import COLORS, FONTS
from gui.widgets import RoundedButton, StyledEntry, StyledCombobox, CardFrame, StatusLabel
from utils.graph_utils import leer_grafo, generar_heuristica, validar_grafo, obtener_estadisticas_grafo
from algorithms.search_algorithms import *
from gui.visualization import VisualizadorGrafo

class InterfazBusquedasIA:
    """
    Clase principal de la interfaz gráfica
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Inteligente de Búsqueda en Grafos")
        self.root.geometry("1500x900")
        self.root.configure(bg=COLORS['bg_dark'])
        
        # Variables principales
        self.grafo = None
        self.heuristica = None
        self.G = None  # Grafo de NetworkX para visualización
        
        # Configurar la interfaz
        self._configurar_estilos()
        self._crear_interfaz()
        
        # Centrar ventana
        self._centrar_ventana()
    
    def _configurar_estilos(self):
        """Configura los estilos de ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para labelframes
        style.configure('Card.TLabelframe',
                       background=COLORS['bg_medium'],
                       foreground=COLORS['text_primary'],
                       bordercolor=COLORS['border'],
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Card.TLabelframe.Label',
                       background=COLORS['bg_medium'],
                       foreground=COLORS['accent_purple'],
                       font=FONTS['subtitle'])
    
    def _centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        # Contenedor principal
        main_container = tk.Frame(self.root, bg=COLORS['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Dividir en dos columnas
        left_panel = tk.Frame(main_container, bg=COLORS['bg_dark'], width=550)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 15))
        left_panel.pack_propagate(False)
        
        right_panel = tk.Frame(main_container, bg=COLORS['bg_dark'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Crear secciones
        self._crear_header(left_panel)
        self._crear_seccion_carga(left_panel)
        self._crear_seccion_config(left_panel)
        self._crear_seccion_acciones(left_panel)
        self._crear_seccion_resultados(left_panel)
        self._crear_seccion_visualizacion(right_panel)
    
    def _crear_header(self, parent):
        """Crea el encabezado con el título"""
        header = CardFrame(parent)
        header.pack(fill=tk.X, pady=(0, 15))
        
        # Contenido del header
        content = tk.Frame(header, bg=COLORS['bg_medium'])
        content.pack(fill=tk.X, padx=20, pady=20)
        
        # Icono y título
        tk.Label(content, text="", font=('Segoe UI', 36),
                bg=COLORS['bg_medium']).pack(side=tk.LEFT, padx=(0, 15))
        
        title_frame = tk.Frame(content, bg=COLORS['bg_medium'])
        title_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(title_frame, text="Búsquedas IA",
                font=FONTS['title'],
                bg=COLORS['bg_medium'],
                fg=COLORS['accent_purple']).pack(anchor='w')
        
        tk.Label(title_frame, text="Sistema de búsqueda en grafos",
                font=FONTS['small'],
                bg=COLORS['bg_medium'],
                fg=COLORS['text_secondary']).pack(anchor='w')
    
    def _crear_seccion_carga(self, parent):
        """Crea la sección de carga de grafos"""
        card = CardFrame(parent, title=" Cargar Grafo")
        card.pack(fill=tk.X, pady=(0, 15))
        
        content = tk.Frame(card, bg=COLORS['bg_medium'])
        content.pack(fill=tk.X, padx=20, pady=15)
        
        # Botón de carga
        btn_cargar = RoundedButton(content, 
                                   text=" Seleccionar Archivo",
                                   command=self.cargar_grafo,
                                   bg_color=COLORS['accent_blue'],
                                   width=180, height=40)
        btn_cargar.pack(side=tk.LEFT, padx=(0, 15))
        
        # Label de estado
        self.lbl_estado_grafo = StatusLabel(content, text="Sin grafo cargado")
        self.lbl_estado_grafo.pack(side=tk.LEFT)
    
    def _crear_seccion_config(self, parent):
        """Crea la sección de configuración"""
        card = CardFrame(parent, title=" Configuración")
        card.pack(fill=tk.X, pady=(0, 15))
        
        content = tk.Frame(card, bg=COLORS['bg_medium'])
        content.pack(fill=tk.BOTH, padx=20, pady=15)
        
        # Algoritmo
        self._crear_campo_config(content, "Algoritmo:", 0)
        self.combo_algoritmo = StyledCombobox(content, width=35, state='readonly')
        self.combo_algoritmo.grid(row=0, column=1, pady=8, sticky='ew', padx=(10, 0))
        self.combo_algoritmo['values'] = [
            'Amplitud (BFS)',
            'Costo Uniforme (Dijkstra)',
            'Profundidad (DFS)',
            'Profundidad Iterativa',
            'Profundidad con Límite',
            'Codicioso (Greedy)',
            'A*',
            'A* Ponderado',
            'Beam Search',
            'Branch and Bound',
            'Hill Climbing',
            'Random Restart Hill Climbing',
            'Simulated Annealing'
        ]
        self.combo_algoritmo.current(0)
        self.combo_algoritmo.bind('<<ComboboxSelected>>', self._mostrar_parametros)
        
        # Nodo inicial
        self._crear_campo_config(content, "Nodo Inicial:", 1)
        self.combo_nodo_inicial = StyledCombobox(content, width=35, state='readonly')
        self.combo_nodo_inicial.grid(row=1, column=1, pady=8, sticky='ew', padx=(10, 0))
        
        # Nodo objetivo
        self._crear_campo_config(content, "Nodo Objetivo:", 2)
        self.combo_nodo_objetivo = StyledCombobox(content, width=35, state='readonly')
        self.combo_nodo_objetivo.grid(row=2, column=1, pady=8, sticky='ew', padx=(10, 0))
        
        # Frame para parámetros adicionales
        self.frame_parametros = tk.Frame(content, bg=COLORS['bg_medium'])
        self.frame_parametros.grid(row=3, column=0, columnspan=2, pady=10, sticky='ew')
        
        content.columnconfigure(1, weight=1)
    
    def _crear_campo_config(self, parent, texto, fila):
        """Crea un label para un campo de configuración"""
        tk.Label(parent, text=texto,
                font=FONTS['heading'],
                bg=COLORS['bg_medium'],
                fg=COLORS['text_primary']).grid(row=fila, column=0, sticky='w', pady=8)
    
    def _crear_seccion_acciones(self, parent):
        """Crea los botones de acción"""
        card = tk.Frame(parent, bg=COLORS['bg_dark'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Botón ejecutar
        btn_ejecutar = RoundedButton(card,
                                     text="▶ EJECUTAR",
                                     command=self.ejecutar_busqueda,
                                     bg_color=COLORS['accent_green'],
                                     width=250, height=50)
        btn_ejecutar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 8))
        
        # Botón comparar
        btn_comparar = RoundedButton(card,
                                     text=" COMPARAR",
                                     command=self.ejecutar_comparativa,
                                     bg_color=COLORS['accent_orange'],
                                     width=250, height=50)
        btn_comparar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(8, 0))
    
    def _crear_seccion_resultados(self, parent):
        """Crea la sección de resultados"""
        card = CardFrame(parent, title=" Resultados")
        card.pack(fill=tk.BOTH, expand=True)
        
        # Área de texto con scroll
        text_frame = tk.Frame(card, bg=COLORS['bg_medium'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        self.text_resultados = scrolledtext.ScrolledText(
            text_frame,
            font=FONTS['code'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_primary'],
            insertbackground=COLORS['accent_purple'],
            relief='flat',
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.text_resultados.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags de colores
        self._configurar_tags_resultados()
    
    def _configurar_tags_resultados(self):
        """Configura los tags de color para el área de resultados"""
        self.text_resultados.tag_config('titulo', 
                                       foreground=COLORS['accent_purple'],
                                       font=FONTS['code_bold'])
        self.text_resultados.tag_config('exito',
                                       foreground=COLORS['accent_green'],
                                       font=FONTS['code_bold'])
        self.text_resultados.tag_config('fallo',
                                       foreground=COLORS['accent_red'],
                                       font=FONTS['code_bold'])
        self.text_resultados.tag_config('info',
                                       foreground=COLORS['text_primary'])
        self.text_resultados.tag_config('camino',
                                       foreground=COLORS['accent_blue'],
                                       font=FONTS['code_bold'])
        self.text_resultados.tag_config('destacado',
                                       foreground=COLORS['accent_orange'],
                                       font=FONTS['code_bold'])
    
    def _crear_seccion_visualizacion(self, parent):
        """Crea la sección de visualización del grafo"""
        card = CardFrame(parent, title=" Visualización del Grafo")
        card.pack(fill=tk.BOTH, expand=True)
        
        # Frame para el canvas de matplotlib
        self.canvas_frame = tk.Frame(card, bg=COLORS['bg_light'])
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Mensaje placeholder
        self.lbl_viz_placeholder = tk.Label(
            self.canvas_frame,
            text="\n\nCarga un grafo para\nvisualizarlo aquí",
            font=('Segoe UI', 18),
            bg=COLORS['bg_light'],
            fg=COLORS['text_secondary']
        )
        self.lbl_viz_placeholder.place(relx=0.5, rely=0.5, anchor='center')
        
        # Crear el visualizador
        self.visualizador = VisualizadorGrafo(self.canvas_frame, COLORS)

# ========== MÉTODOS DE LÓGICA ==========
    
    def _mostrar_parametros(self, event=None):
        """Muestra campos adicionales según el algoritmo seleccionado"""
        # Limpiar parámetros anteriores
        for widget in self.frame_parametros.winfo_children():
            widget.destroy()
        
        algoritmo = self.combo_algoritmo.get()
        
        if algoritmo == 'Profundidad con Límite':
            self._crear_parametro_numero("Límite:", "5", 'entry_limite')
            
        elif algoritmo == 'A* Ponderado':
            self._crear_parametro_numero("Peso W:", "1.3", 'entry_peso')
            
        elif algoritmo == 'Beam Search':
            self._crear_parametro_numero("Ancho haz:", "2", 'entry_ancho')
            
        elif algoritmo == 'Random Restart Hill Climbing':
            self._crear_parametro_numero("Reinicios:", "3", 'entry_reinicios')
            
        elif algoritmo == 'Simulated Annealing':
            self._crear_parametro_numero("Temperatura:", "100", 'entry_temperatura')
    
    def _crear_parametro_numero(self, label_text, valor_default, attr_name):
        """Crea un campo numérico para parámetros"""
        tk.Label(self.frame_parametros, text=label_text,
                font=FONTS['body'],
                bg=COLORS['bg_medium'],
                fg=COLORS['text_primary']).grid(row=0, column=0, sticky='w', padx=5)
        
        entry = StyledEntry(self.frame_parametros, width=80)
        entry.insert(0, valor_default)
        entry.grid(row=0, column=1, padx=5, sticky='ew')
        
        # Guardar referencia
        setattr(self, attr_name, entry)
        
        self.frame_parametros.columnconfigure(1, weight=1)
    
    def cargar_grafo(self):
        """Carga un grafo desde un archivo"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de grafo",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if not archivo:
            return
        
        try:
            # Leer el grafo
            self.grafo = leer_grafo(archivo)
            
            # Validar el grafo
            es_valido, mensaje = validar_grafo(self.grafo)
            if not es_valido:
                messagebox.showerror("Error", f"Grafo inválido:\n{mensaje}")
                return
            
            # Obtener estadísticas
            stats = obtener_estadisticas_grafo(self.grafo)
            
            # Actualizar comboboxes de nodos
            nodos = sorted(self.grafo.keys())
            self.combo_nodo_inicial['values'] = nodos
            self.combo_nodo_objetivo['values'] = nodos
            
            if nodos:
                self.combo_nodo_inicial.current(0)
                self.combo_nodo_objetivo.current(min(1, len(nodos)-1))
            
            # Actualizar estado
            self.lbl_estado_grafo.set_status(
                f"{stats['num_nodos']} nodos, {stats['num_aristas']} aristas",
                'success'
            )
            
            # Crear grafo NetworkX para visualización
            self.G = nx.Graph()
            for nodo, vecinos in self.grafo.items():
                for vecino, peso in vecinos.items():
                    self.G.add_edge(nodo, vecino, weight=peso)
            
            # Visualizar
            self.lbl_viz_placeholder.place_forget()
            self.visualizador.dibujar_grafo(self.G)
            
            # Mostrar info en resultados
            self._mostrar_info_grafo(stats, nodos)
            
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
            self.lbl_estado_grafo.set_status("Archivo no encontrado", 'error')
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar:\n{str(e)}")
            self.lbl_estado_grafo.set_status("Error al cargar", 'error')
    
    def _mostrar_info_grafo(self, stats, nodos):
        """Muestra información del grafo cargado"""
        self.text_resultados.delete(1.0, tk.END)
        self.text_resultados.insert(tk.END, "═" * 60 + "\n")
        self.text_resultados.insert(tk.END, "GRAFO CARGADO EXITOSAMENTE\n", 'titulo')
        self.text_resultados.insert(tk.END, "═" * 60 + "\n\n")
        
        self.text_resultados.insert(tk.END, " Estadísticas:\n", 'destacado')
        self.text_resultados.insert(tk.END, f"  • Nodos: {stats['num_nodos']}\n", 'info')
        self.text_resultados.insert(tk.END, f"  • Aristas: {stats['num_aristas']}\n", 'info')
        self.text_resultados.insert(tk.END, f"  • Grado promedio: {stats['grado_promedio']:.2f}\n", 'info')
        self.text_resultados.insert(tk.END, f"  • Peso promedio: {stats['peso_promedio']:.2f}\n\n", 'info')
        
        self.text_resultados.insert(tk.END, " Nodos disponibles:\n", 'destacado')
        for i, nodo in enumerate(nodos[:15]):
            self.text_resultados.insert(tk.END, f"  • {nodo}\n", 'info')
        if len(nodos) > 15:
            self.text_resultados.insert(tk.END, f"  ... y {len(nodos)-15} más\n", 'info')
    
    def ejecutar_busqueda(self):
        """Ejecuta el algoritmo de búsqueda seleccionado"""
        # Validar que hay un grafo cargado
        if self.grafo is None:
            messagebox.showwarning("Advertencia", "Primero debes cargar un grafo")
            return
        
        # Obtener parámetros
        algoritmo = self.combo_algoritmo.get()
        nodo_ini = self.combo_nodo_inicial.get()
        nodo_fin = self.combo_nodo_objetivo.get()
        
        # Validar nodos
        if not nodo_ini or not nodo_fin:
            messagebox.showwarning("Advertencia", 
                                 "Debes seleccionar nodos inicial y objetivo")
            return
        
        if nodo_ini not in self.grafo:
            messagebox.showerror("Error", f"El nodo '{nodo_ini}' no existe en el grafo")
            return
        
        if nodo_fin not in self.grafo:
            messagebox.showerror("Error", f"El nodo '{nodo_fin}' no existe en el grafo")
            return
        
        # Mostrar info inicial
        self._mostrar_header_ejecucion(algoritmo, nodo_ini, nodo_fin)
        self.root.update()
        
        try:
            # Ejecutar algoritmo
            tiempo_inicio = time.time()
            resultado = self._ejecutar_algoritmo(algoritmo, nodo_ini, nodo_fin)
            tiempo_fin = time.time()
            tiempo_ejecucion = tiempo_fin - tiempo_inicio
            
            # Mostrar resultado
            self._mostrar_resultado(resultado, nodo_ini, nodo_fin, tiempo_ejecucion)
            
            # Actualizar visualización
            if resultado['exito']:
                self.visualizador.dibujar_grafo(self.G, resultado['camino'])
            
        except ValueError as e:
            messagebox.showerror("Error", f"Parámetro inválido:\n{str(e)}")
            self.text_resultados.insert(tk.END, f"\n Error: {str(e)}\n", 'fallo')
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar:\n{str(e)}")
            self.text_resultados.insert(tk.END, f"\n Error: {str(e)}\n", 'fallo')
    
    def _ejecutar_algoritmo(self, algoritmo, nodo_ini, nodo_fin):
        """Ejecuta el algoritmo seleccionado y retorna el resultado"""
        if algoritmo == 'Amplitud (BFS)':
            return busqueda_amplitud(self.grafo, nodo_ini, nodo_fin)
        
        elif algoritmo == 'Costo Uniforme (Dijkstra)':
            return busqueda_costo_uniforme(self.grafo, nodo_ini, nodo_fin)
        
        elif algoritmo == 'Profundidad (DFS)':
            return busqueda_profundidad(self.grafo, nodo_ini, nodo_fin)
        
        elif algoritmo == 'Profundidad Iterativa':
            return busqueda_profundidad_iterativa(self.grafo, nodo_ini, nodo_fin)
        
        elif algoritmo == 'Profundidad con Límite':
            limite = self._validar_parametro_int('entry_limite', 'Límite')
            return busqueda_profundidad_limitada(self.grafo, nodo_ini, nodo_fin, limite)
        
        elif algoritmo == 'Codicioso (Greedy)':
            self.heuristica = generar_heuristica(self.grafo, nodo_fin)
            return busqueda_codiciosa(self.grafo, nodo_ini, nodo_fin, self.heuristica)
        
        elif algoritmo == 'A*':
            self.heuristica = generar_heuristica(self.grafo, nodo_fin)
            return busqueda_a_estrella(self.grafo, nodo_ini, nodo_fin, self.heuristica)
        
        elif algoritmo == 'A* Ponderado':
            peso_w = self._validar_parametro_float('entry_peso', 'Peso W')
            self.heuristica = generar_heuristica(self.grafo, nodo_fin)
            return busqueda_a_estrella_ponderado(self.grafo, nodo_ini, nodo_fin, 
                                                self.heuristica, peso_w)
        
        elif algoritmo == 'Beam Search':
            ancho_haz = self._validar_parametro_int('entry_ancho', 'Ancho haz')
            self.heuristica = generar_heuristica(self.grafo, nodo_fin)
            return busqueda_beam(self.grafo, nodo_ini, nodo_fin, 
                               self.heuristica, ancho_haz)
        
        elif algoritmo == 'Branch and Bound':
            return busqueda_branch_and_bound(self.grafo, nodo_ini, nodo_fin)
        
        elif algoritmo == 'Hill Climbing':
            self.heuristica = generar_heuristica(self.grafo, nodo_fin)
            return busqueda_hill_climbing(self.grafo, nodo_ini, nodo_fin, self.heuristica)
        
        elif algoritmo == 'Random Restart Hill Climbing':
            max_reinicios = self._validar_parametro_int('entry_reinicios', 'Reinicios')
            self.heuristica = generar_heuristica(self.grafo, nodo_fin)
            return busqueda_random_restart_hill_climbing(self.grafo, nodo_ini, nodo_fin, 
                                                        self.heuristica, max_reinicios)
        
        elif algoritmo == 'Simulated Annealing':
            temperatura = self._validar_parametro_float('entry_temperatura', 'Temperatura')
            self.heuristica = generar_heuristica(self.grafo, nodo_fin)
            return busqueda_simulated_annealing(self.grafo, nodo_ini, nodo_fin, 
                                              self.heuristica, temperatura)
    
    def _validar_parametro_int(self, attr_name, nombre_param):
        """Valida y obtiene un parámetro entero"""
        try:
            valor = int(getattr(self, attr_name).get())
            if valor <= 0:
                raise ValueError(f"{nombre_param} debe ser mayor que 0")
            return valor
        except ValueError:
            raise ValueError(f"{nombre_param} debe ser un número entero válido")
    
    def _validar_parametro_float(self, attr_name, nombre_param):
        """Valida y obtiene un parámetro float"""
        try:
            valor = float(getattr(self, attr_name).get())
            if valor <= 0:
                raise ValueError(f"{nombre_param} debe ser mayor que 0")
            return valor
        except ValueError:
            raise ValueError(f"{nombre_param} debe ser un número válido")
    
    def _mostrar_header_ejecucion(self, algoritmo, nodo_ini, nodo_fin):
        """Muestra el encabezado de la ejecución"""
        self.text_resultados.delete(1.0, tk.END)
        self.text_resultados.insert(tk.END, "═" * 60 + "\n")
        self.text_resultados.insert(tk.END, f"{algoritmo}\n", 'titulo')
        self.text_resultados.insert(tk.END, "═" * 60 + "\n\n")
        self.text_resultados.insert(tk.END, f" Inicio: {nodo_ini}\n", 'info')
        self.text_resultados.insert(tk.END, f" Objetivo: {nodo_fin}\n\n", 'info')
    
    def _mostrar_resultado(self, resultado, nodo_ini, nodo_fin, tiempo_ejecucion):
        """Muestra el resultado de la búsqueda"""
        self.text_resultados.insert(tk.END, "─" * 60 + "\n")
        
        if resultado['exito']:
            self.text_resultados.insert(tk.END, " CAMINO ENCONTRADO\n", 'exito')
            self.text_resultados.insert(tk.END, "─" * 60 + "\n\n")
            
            self.text_resultados.insert(tk.END, "  Camino:\n", 'destacado')
            camino_str = " → ".join(resultado['camino'])
            self.text_resultados.insert(tk.END, f"{camino_str}\n\n", 'camino')
            
            self.text_resultados.insert(tk.END, f" Costo total: {resultado['costo']:.2f}\n", 'info')
            self.text_resultados.insert(tk.END, f" Nodos expandidos: {resultado['nodos_expandidos']}\n", 'info')
            self.text_resultados.insert(tk.END, f" Longitud del camino: {len(resultado['camino'])} nodos\n", 'info')
            self.text_resultados.insert(tk.END, f"  Tiempo de ejecución: {tiempo_ejecucion:.6f}s\n", 'info')
        else:
            self.text_resultados.insert(tk.END, " NO SE ENCONTRÓ CAMINO\n", 'fallo')
            self.text_resultados.insert(tk.END, "─" * 60 + "\n\n")
            self.text_resultados.insert(tk.END, 
                f"No existe una ruta de '{nodo_ini}' a '{nodo_fin}'\n\n", 'info')
            self.text_resultados.insert(tk.END, 
                f" Nodos expandidos: {resultado['nodos_expandidos']}\n", 'info')
            
            if resultado['camino']:
                self.text_resultados.insert(tk.END, f"\nCamino parcial explorado:\n", 'destacado')
                camino_str = " → ".join(resultado['camino'])
                self.text_resultados.insert(tk.END, f"{camino_str}\n", 'camino')
        
        self.text_resultados.insert(tk.END, "\n" + "═" * 60 + "\n")
    
    def ejecutar_comparativa(self):
        """Abre diálogo para seleccionar tipo de comparación"""
        if self.grafo is None:
            messagebox.showwarning("Advertencia", "Primero debes cargar un grafo")
            return
        
        nodo_ini = self.combo_nodo_inicial.get()
        nodo_fin = self.combo_nodo_objetivo.get()
        
        if not nodo_ini or not nodo_fin:
            messagebox.showwarning("Advertencia",
                                 "Debes seleccionar nodos inicial y objetivo")
            return
        
        # Crear ventana de selección
        self._mostrar_dialogo_comparativa(nodo_ini, nodo_fin)
    
    def _mostrar_dialogo_comparativa(self, nodo_ini, nodo_fin):
        """Muestra el diálogo de selección de tipo de comparativa"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Tipo de Comparación")
        ventana.geometry("450x300")
        ventana.configure(bg=COLORS['bg_dark'])
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - 225
        y = (ventana.winfo_screenheight() // 2) - 150
        ventana.geometry(f"450x300+{x}+{y}")
        
        # Título
        tk.Label(ventana, text="Selecciona el tipo de búsquedas",
                font=FONTS['subtitle'],
                bg=COLORS['bg_dark'],
                fg=COLORS['text_primary']).pack(pady=30)
        
        # Botones
        def comparar_no_informadas():
            ventana.destroy()
            self._ejecutar_comparacion(nodo_ini, nodo_fin, 'no_informadas')
        
        def comparar_informadas():
            ventana.destroy()
            self._ejecutar_comparacion(nodo_ini, nodo_fin, 'informadas')
        
        RoundedButton(ventana,
                     text="🔍 Búsquedas NO Informadas",
                     command=comparar_no_informadas,
                     bg_color=COLORS['accent_blue'],
                     width=350, height=55).pack(pady=10)
        
        RoundedButton(ventana,
                     text="🧭 Búsquedas Informadas",
                     command=comparar_informadas,
                     bg_color=COLORS['accent_purple'],
                     width=350, height=55).pack(pady=10)
    
    def _ejecutar_comparacion(self, nodo_ini, nodo_fin, tipo):
        """Ejecuta la comparación de algoritmos"""
        self.text_resultados.delete(1.0, tk.END)
        self.text_resultados.insert(tk.END, "═" * 60 + "\n")
        self.text_resultados.insert(tk.END, "MODO COMPARATIVA\n", 'titulo')
        self.text_resultados.insert(tk.END, "═" * 60 + "\n\n")
        self.text_resultados.insert(tk.END, f"Comparando algoritmos de: {nodo_ini} → {nodo_fin}\n\n", 'info')
        
        self.root.update()
        
        # Preparar algoritmos según el tipo
        if tipo == 'no_informadas':
            algoritmos = self._obtener_algoritmos_no_informados(nodo_ini, nodo_fin)
        else:
            algoritmos = self._obtener_algoritmos_informados(nodo_ini, nodo_fin)
        
        # Ejecutar todos los algoritmos
        resultados = []
        for nombre, funcion in algoritmos:
            self.text_resultados.insert(tk.END, f"⏳ Ejecutando {nombre}...\n", 'destacado')
            self.root.update()
            
            try:
                tiempo_inicio = time.time()
                resultado = funcion()
                tiempo_fin = time.time()
                tiempo = tiempo_fin - tiempo_inicio
                
                resultados.append({
                    'nombre': nombre,
                    'resultado': resultado,
                    'tiempo': tiempo,
                    'exito': resultado['exito']
                })
            except Exception as e:
                resultados.append({
                    'nombre': nombre,
                    'resultado': None,
                    'tiempo': 0,
                    'exito': False,
                    'error': str(e)
                })
        
        # Mostrar resultados de la comparación
        self._mostrar_resultados_comparativa(resultados)
    
    def _obtener_algoritmos_no_informados(self, nodo_ini, nodo_fin):
        """Retorna lista de algoritmos no informados"""
        return [
            ('Amplitud (BFS)', 
             lambda: busqueda_amplitud(self.grafo, nodo_ini, nodo_fin)),
            ('Costo Uniforme', 
             lambda: busqueda_costo_uniforme(self.grafo, nodo_ini, nodo_fin)),
            ('Profundidad (DFS)', 
             lambda: busqueda_profundidad(self.grafo, nodo_ini, nodo_fin)),
            ('Profundidad Iterativa', 
             lambda: busqueda_profundidad_iterativa(self.grafo, nodo_ini, nodo_fin, 5)),
            ('Branch & Bound', 
             lambda: busqueda_branch_and_bound(self.grafo, nodo_ini, nodo_fin))
        ]
    
    def _obtener_algoritmos_informados(self, nodo_ini, nodo_fin):
        """Retorna lista de algoritmos informados"""
        heuristica = generar_heuristica(self.grafo, nodo_fin)
        
        return [
            ('Codicioso (Greedy)', 
             lambda: busqueda_codiciosa(self.grafo, nodo_ini, nodo_fin, heuristica)),
            ('A*', 
             lambda: busqueda_a_estrella(self.grafo, nodo_ini, nodo_fin, heuristica)),
            ('A* Ponderado', 
             lambda: busqueda_a_estrella_ponderado(self.grafo, nodo_ini, nodo_fin, heuristica, 1.3)),
            ('Beam Search', 
             lambda: busqueda_beam(self.grafo, nodo_ini, nodo_fin, heuristica, 2)),
            ('Hill Climbing', 
             lambda: busqueda_hill_climbing(self.grafo, nodo_ini, nodo_fin, heuristica))
        ]
    
    def _mostrar_resultados_comparativa(self, resultados):
        """Muestra los resultados de la comparativa"""
        self.text_resultados.insert(tk.END, "\n" + "═" * 60 + "\n")
        self.text_resultados.insert(tk.END, "RESULTADOS DE LA COMPARACIÓN\n", 'titulo')
        self.text_resultados.insert(tk.END, "═" * 60 + "\n\n")
        
        # Filtrar solo los exitosos
        exitosos = [r for r in resultados if r['exito']]
        
        if exitosos:
            # Encontrar los mejores
            mas_rapido = min(exitosos, key=lambda x: x['tiempo'])
            menor_costo = min(exitosos, key=lambda x: x['resultado']['costo'])
            menos_nodos = min(exitosos, key=lambda x: x['resultado']['nodos_expandidos'])
            
            # Mostrar ganadores
            self.text_resultados.insert(tk.END, "🏆 GANADORES\n", 'destacado')
            self.text_resultados.insert(tk.END, "─" * 60 + "\n\n")
            
            self.text_resultados.insert(tk.END, "⚡ MÁS RÁPIDO: ", 'destacado')
            self.text_resultados.insert(tk.END, 
                f"{mas_rapido['nombre']} ({mas_rapido['tiempo']:.6f}s)\n\n", 'exito')
            
            self.text_resultados.insert(tk.END, " MENOR COSTO: ", 'destacado')
            self.text_resultados.insert(tk.END, 
                f"{menor_costo['nombre']} (costo: {menor_costo['resultado']['costo']:.2f})\n\n", 'exito')
            
            self.text_resultados.insert(tk.END, " MENOS NODOS EXPANDIDOS: ", 'destacado')
            self.text_resultados.insert(tk.END, 
                f"{menos_nodos['nombre']} ({menos_nodos['resultado']['nodos_expandidos']} nodos)\n\n", 'exito')
            
            # Tabla detallada
            self.text_resultados.insert(tk.END, "─" * 60 + "\n")
            self.text_resultados.insert(tk.END, " DETALLES DE TODOS LOS ALGORITMOS\n\n", 'destacado')
            
            for r in resultados:
                if r['exito']:
                    self.text_resultados.insert(tk.END, f"✓ {r['nombre']}:\n", 'exito')
                    self.text_resultados.insert(tk.END, 
                        f"   Tiempo: {r['tiempo']:.6f}s | "
                        f"Costo: {r['resultado']['costo']:.2f} | "
                        f"Nodos: {r['resultado']['nodos_expandidos']}\n\n", 'info')
                else:
                    self.text_resultados.insert(tk.END, f"✗ {r['nombre']}: ", 'fallo')
                    error_msg = r.get('error', 'Sin solución')
                    self.text_resultados.insert(tk.END, f"{error_msg}\n\n", 'info')
            
            # Visualizar el mejor camino
            self.visualizador.dibujar_grafo(self.G, menor_costo['resultado']['camino'])
            
        else:
            self.text_resultados.insert(tk.END, 
                "❌ Ningún algoritmo encontró una solución\n\n", 'fallo')
        
        self.text_resultados.insert(tk.END, "═" * 60 + "\n")