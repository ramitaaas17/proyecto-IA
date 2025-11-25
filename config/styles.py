"""
Configuración de estilos y colores para la aplicación
Aquí se definen todos los colores y fuentes que usaremos
"""

# Paleta de colores oscura y moderna
COLORS = {
    'bg_dark': '#0d1117',           # Fondo oscuro principal
    'bg_medium': '#161b22',         # Fondo medio para cards
    'bg_light': '#1c2128',          # Fondo claro para inputs
    'accent_blue': '#58a6ff',       # Azul para elementos importantes
    'accent_purple': '#bc8cff',     # Morado para acentos
    'accent_green': '#3fb950',      # Verde para éxito
    'accent_orange': '#ff9800',     # Naranja para alertas
    'accent_red': '#f85149',        # Rojo para errores
    'text_primary': '#e6edf3',      # Texto principal
    'text_secondary': '#8b949e',    # Texto secundario
    'border': '#30363d',            # Color de bordes
    'hover': '#21262d'              # Color al pasar mouse
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