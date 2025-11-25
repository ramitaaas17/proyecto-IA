"""
Configuración de estilos y colores para la aplicación
Aquí se definen todos los colores y fuentes que usaremos
"""

# Paleta de colores clara y cálida - Fondo claro, texto oscuro
COLORS = {
    'bg_dark': '#fff5e6',           # Fondo crema muy claro
    'bg_medium': '#ffe9cc',         # Fondo durazno suave
    'bg_light': '#ffffff',          # Blanco puro para inputs
    'accent_blue': '#2196F3',       # Azul vibrante
    'accent_purple': '#9C27B0',     # Morado vibrante
    'accent_green': '#4CAF50',      # Verde vibrante
    'accent_orange': '#FF6F00',     # Naranja intenso
    'accent_red': '#f44336',        # Rojo vibrante
    'text_primary': '#2c1810',      # Texto café oscuro
    'text_secondary': '#5d4037',    # Texto café medio
    'border': '#d4a574',            # Borde durazno/canela
    'hover': '#fff0db'              # Hover amarillo suave
}

# Fuentes para toda la aplicación
FONTS = {
    'title': ('Segoe UI', 22, 'bold'),
    'subtitle': ('Segoe UI', 14, 'bold'),
    'heading': ('Segoe UI', 12, 'bold'),
    'body': ('Segoe UI', 10),
    'small': ('Segoe UI', 9),
    'code': ('Consolas', 9),
    'code_bold': ('Consolas', 10, 'bold')
}

# Configuración de bordes redondeados y espaciado
SPACING = {
    'small': 5,
    'medium': 10,
    'large': 15,
    'xlarge': 20
}

# Configuración de tamaños de botones
BUTTON_CONFIG = {
    'padding_x': 25,
    'padding_y': 12,
    'border_width': 0,
    'relief': 'flat',
    'cursor': 'hand2'
}

# Configuración de entradas de texto
ENTRY_CONFIG = {
    'border_width': 1,
    'relief': 'solid',
    'padding': 8
}