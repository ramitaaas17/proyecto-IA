"""
Widgets personalizados con diseño moderno
Botones, entradas y otros elementos con bordes redondeados
"""

import tkinter as tk
from tkinter import ttk
from config.styles import COLORS, FONTS, BUTTON_CONFIG, ENTRY_CONFIG

class RoundedButton(tk.Canvas):
    """
    Botón con bordes redondeados y efectos hover
    """
    def __init__(self, parent, text, command=None, bg_color=COLORS['accent_blue'], 
                 text_color='white', width=150, height=45, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        bg=COLORS['bg_dark'], highlightthickness=0)
        
        self.command = command
        self.bg_color = bg_color
        self.hover_color = self._darken_color(bg_color)
        self.text_color = text_color
        self.width = width
        self.height = height
        self.is_hovered = False
        
        # Crear el rectángulo redondeado
        self.create_rounded_rectangle(5, 5, width-5, height-5, 
                                      radius=10, fill=bg_color, 
                                      outline='', tags='button')
        
        # Crear el texto
        self.create_text(width//2, height//2, text=text, 
                        fill=text_color, font=FONTS['heading'], 
                        tags='text')
        
        # Eventos de mouse
        self.tag_bind('button', '<Button-1>', self._on_click)
        self.tag_bind('text', '<Button-1>', self._on_click)
        self.tag_bind('button', '<Enter>', self._on_enter)
        self.tag_bind('text', '<Enter>', self._on_enter)
        self.tag_bind('button', '<Leave>', self._on_leave)
        self.tag_bind('text', '<Leave>', self._on_leave)
        
        # Cambiar cursor
        self.configure(cursor='hand2')
    
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=10, **kwargs):
        """Crea un rectángulo con esquinas redondeadas"""
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _darken_color(self, color):
        """Oscurece un color hex para el efecto hover"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darker = tuple(max(0, int(c * 0.8)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*darker)
    
    def _on_click(self, event):
        """Ejecuta el comando al hacer click"""
        if self.command:
            self.command()
    
    def _on_enter(self, event):
        """Efecto hover al entrar"""
        self.itemconfig('button', fill=self.hover_color)
        self.is_hovered = True
    
    def _on_leave(self, event):
        """Quita el efecto hover al salir"""
        self.itemconfig('button', fill=self.bg_color)
        self.is_hovered = False
    
    def set_enabled(self, enabled):
        """Habilita o deshabilita el botón"""
        if enabled:
            self.itemconfig('button', fill=self.bg_color)
            self.configure(cursor='hand2')
        else:
            self.itemconfig('button', fill=COLORS['text_secondary'])
            self.configure(cursor='arrow')

class StyledEntry(tk.Frame):
    """
    Campo de entrada con estilo moderno
    """
    def __init__(self, parent, placeholder="", width=200, **kwargs):
        super().__init__(parent, bg=COLORS['bg_dark'])
        
        self.placeholder = placeholder
        self.has_placeholder = False
        
        # Frame contenedor con borde
        self.entry_frame = tk.Frame(self, bg=COLORS['border'], 
                                    highlightthickness=0)
        self.entry_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Campo de entrada
        self.entry = tk.Entry(self.entry_frame, 
                             font=FONTS['body'],
                             bg=COLORS['bg_light'],
                             fg=COLORS['text_primary'],
                             insertbackground=COLORS['accent_blue'],
                             relief='flat',
                             width=width//10,
                             **kwargs)
        self.entry.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)
        
        # Placeholder
        if placeholder:
            self._show_placeholder()
        
        # Eventos
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        self.entry.bind('<Enter>', self._on_enter)
        self.entry.bind('<Leave>', self._on_leave)
    
    def _show_placeholder(self):
        """Muestra el texto placeholder"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg=COLORS['text_secondary'])
        self.has_placeholder = True
    
    def _hide_placeholder(self):
        """Oculta el texto placeholder"""
        if self.has_placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=COLORS['text_primary'])
            self.has_placeholder = False
    
    def _on_focus_in(self, event):
        """Al hacer foco en el campo"""
        self._hide_placeholder()
        self.entry_frame.config(bg=COLORS['accent_blue'])
    
    def _on_focus_out(self, event):
        """Al perder el foco"""
        self.entry_frame.config(bg=COLORS['border'])
        if not self.entry.get():
            self._show_placeholder()
    
    def _on_enter(self, event):
        """Hover effect"""
        if self.entry_frame['bg'] != COLORS['accent_blue']:
            self.entry_frame.config(bg=COLORS['hover'])
    
    def _on_leave(self, event):
        """Salir del hover"""
        if self.entry_frame['bg'] != COLORS['accent_blue']:
            self.entry_frame.config(bg=COLORS['border'])
    
    def get(self):
        """Obtiene el valor del campo"""
        if self.has_placeholder:
            return ""
        return self.entry.get()
    
    def insert(self, index, text):
        """Inserta texto en el campo"""
        self._hide_placeholder()
        self.entry.insert(index, text)

class StyledCombobox(ttk.Combobox):
    """
    Combobox con estilo moderno
    """
    def __init__(self, parent, **kwargs):
        style = ttk.Style()
        
        # Configurar estilo del combobox
        style.configure('Styled.TCombobox',
                       fieldbackground=COLORS['bg_light'],
                       background=COLORS['bg_medium'],
                       foreground=COLORS['text_primary'],
                       arrowcolor=COLORS['accent_blue'],
                       bordercolor=COLORS['border'],
                       lightcolor=COLORS['bg_light'],
                       darkcolor=COLORS['bg_medium'])
        
        super().__init__(parent, style='Styled.TCombobox', **kwargs)
        
        # Configurar fuente
        self.configure(font=FONTS['body'])

class CardFrame(tk.Frame):
    """
    Frame estilo card con sombra y bordes redondeados
    """
    def __init__(self, parent, title="", **kwargs):
        super().__init__(parent, bg=COLORS['bg_medium'], 
                        highlightbackground=COLORS['border'],
                        highlightthickness=1, **kwargs)
        
        if title:
            # Frame para el título
            title_frame = tk.Frame(self, bg=COLORS['bg_medium'])
            title_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
            
            # Línea decorativa
            tk.Canvas(title_frame, width=4, height=20, 
                     bg=COLORS['accent_purple'], 
                     highlightthickness=0).pack(side=tk.LEFT)
            
            # Título
            tk.Label(title_frame, text=title,
                    font=FONTS['subtitle'],
                    bg=COLORS['bg_medium'],
                    fg=COLORS['text_primary']).pack(side=tk.LEFT, padx=10)
            
            # Línea separadora
            tk.Frame(self, height=1, bg=COLORS['border']).pack(fill=tk.X, padx=15)

class StatusLabel(tk.Label):
    """
    Label de estado con indicador de color
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 
                        font=FONTS['small'],
                        bg=COLORS['bg_dark'],
                        fg=COLORS['text_secondary'],
                        **kwargs)
    
    def set_status(self, text, status_type='info'):
        """
        Actualiza el estado con color
        status_type puede ser: 'info', 'success', 'warning', 'error'
        """
        icons = {
            'info': 'ℹ️',
            'success': '✓',
            'warning': '⚠',
            'error': '✗'
        }
        
        colors = {
            'info': COLORS['text_secondary'],
            'success': COLORS['accent_green'],
            'warning': COLORS['accent_orange'],
            'error': COLORS['accent_red']
        }
        
        icon = icons.get(status_type, '')
        color = colors.get(status_type, COLORS['text_secondary'])
        
        self.config(text=f"{icon} {text}", fg=color)