"""
Archivo principal de la aplicación
Ejecuta este archivo para iniciar el sistema de búsquedas IA
"""

import tkinter as tk
from gui.main_window import InterfazBusquedasIA

def main():
    """
    Función principal que inicia la aplicación
    """
    # Crear la ventana principal de tkinter
    root = tk.Tk()
    
    # Inicializar la interfaz gráfica
    app = InterfazBusquedasIA(root)
    
    # Iniciar el loop de eventos de tkinter
    root.mainloop()

if __name__ == "__main__":
    main()