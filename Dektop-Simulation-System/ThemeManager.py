from typing import Dict

class ThemeManager:
    """Manage application themes."""
    
    LIGHT_THEME = {
        'bg': '#f0f0f0',
        'fg': '#000000',
        'button_bg': '#e0e0e0',
        'button_fg': '#000000',
        'button_active_bg': '#d0d0d0',
        'button_active_fg': '#000000',
        'tree_bg': '#ffffff',
        'tree_fg': '#000000',
        'header_bg': '#e0e0e0',
        'header_fg': '#000000',
        'frame_bg': '#ffffff',
        'entry_bg': '#ffffff',
        'entry_fg': '#000000',
        'graph_bg': '#ffffff',
        'graph_fg': '#000000',
        'grid_color': '#cccccc',
        'scrollbar_bg': '#e0e0e0',
        'scrollbar_trough': '#d0d0d0',
        'scrollbar_arrow': '#000000',
        'selected_bg': '#c0c0c0',
        'selected_fg': '#000000',
        'tab_bg': '#e0e0e0',
        'tab_fg': '#000000',
        'tab_selected_bg': '#d0d0d0',
        'tab_selected_fg': '#000000',
        'toggle_bg': '#e0e0e0',
        'toggle_fg': '#000000',
        'toggle_selected_bg': '#c0c0c0',
        'toggle_selected_fg': '#000000',
        'toggle_active_bg': '#d0d0d0',
        'toggle_active_fg': '#000000',
        'tooltip_bg': '#ffffff',
        'tooltip_fg': '#000000'
    }
    
    DARK_THEME = {
        'bg': '#2d2d2d',
        'fg': '#ffffff',
        'button_bg': '#404040',
        'button_fg': '#ffffff',
        'button_active_bg': '#505050',
        'button_active_fg': '#ffffff',
        'tree_bg': '#333333',
        'tree_fg': '#ffffff',
        'header_bg': '#404040',
        'header_fg': '#ffffff',
        'frame_bg': '#333333',
        'entry_bg': '#404040',
        'entry_fg': '#ffffff',
        'graph_bg': '#333333',
        'graph_fg': '#ffffff',
        'grid_color': '#505050',
        'scrollbar_bg': '#404040',
        'scrollbar_trough': '#333333',
        'scrollbar_arrow': '#ffffff',
        'selected_bg': '#505050',
        'selected_fg': '#ffffff',
        'tab_bg': '#404040',
        'tab_fg': '#ffffff',
        'tab_selected_bg': '#505050',
        'tab_selected_fg': '#ffffff',
        'toggle_bg': '#404040',
        'toggle_fg': '#ffffff',
        'toggle_selected_bg': '#505050',
        'toggle_selected_fg': '#ffffff',
        'toggle_active_bg': '#606060',
        'toggle_active_fg': '#ffffff',
        'tooltip_bg': '#333333',
        'tooltip_fg': '#ffffff'
    }
    
    @classmethod
    def get_theme(cls, is_dark: bool) -> Dict[str, str]:
        """Get the current theme colors."""
        return cls.DARK_THEME if is_dark else cls.LIGHT_THEME



# def setup_style(self) -> None:
#         """Configure the application style to apply dark or light theme consistently across all widgets."""
#         style = ttk.Style()
#         theme = ThemeManager.get_theme(self.is_dark_mode)

#         # Base Frame style
#         style.configure("TFrame", background=theme['bg'])
#         style.configure("TLabelFrame", background=theme['bg'], foreground=theme['fg'], padding=10)
#         style.configure("TLabelFrame.Label", background=theme['bg'], foreground=theme['fg'])

#         # Label style
#         style.configure("TLabel", background=theme['bg'], foreground=theme['fg'])

#         # Entry (input field) style
#         style.configure("TEntry", 
#                         fieldbackground=theme['entry_bg'], 
#                         foreground=theme['fg'], 
#                         background=theme['entry_bg'])
        
#         style.configure("ControlFrame.TButton",
#                     background=theme['button_bg'],
#                     foreground=theme['button_fg'],
#                     padding=5)
#         style.map("ControlFrame.TButton",
#               background=[("active", theme['button_active_bg'])],
#               foreground=[("active", theme['button_active_fg'])])

#         # Button style
#         style.configure("TButton", 
#                         background=theme['button_bg'], 
#                         foreground=theme['button_fg'], 
#                         padding=5)
#         style.map("TButton", 
#                 background=[("active", theme['button_active_bg'])],
#                 foreground=[("active", theme['button_active_fg'])])

#         # Toggle Button style
#         style.configure("Toggle.TButton", 
#                         background=theme['toggle_bg'], 
#                         foreground=theme['toggle_fg'], 
#                         padding=5, 
#                         width=3)
#         style.map("Toggle.TButton", 
#                 background=[("active", theme['toggle_selected_bg']), ("active", theme['toggle_active_bg'])],
#                 foreground=[("active", theme['toggle_selected_fg']), ("active", theme['toggle_active_fg'])])

#         # Treeview style
#         style.configure("Treeview", 
#                         background=theme['bg'], 
#                         fieldbackground=theme['bg'], 
#                         foreground=theme['fg'])
#         style.map("Treeview", 
#                 background=[("selected", theme['selected_bg'])], 
#                 foreground=[("selected", theme['selected_fg'])])
#         style.configure("Treeview.Heading", 
#                         background=theme['header_bg'], 
#                         foreground=theme['header_fg'], 
#                         font=("Helvetica", 10, "bold"))

#         # Scrollbar style
#         style.configure("Vertical.TScrollbar", 
#                         background=theme['scrollbar_bg'], 
#                         troughcolor=theme['scrollbar_trough'], 
#                         arrowcolor=theme['scrollbar_arrow'])
#         style.configure("Horizontal.TScrollbar", 
#                         background=theme['scrollbar_bg'], 
#                         troughcolor=theme['scrollbar_trough'], 
#                         arrowcolor=theme['scrollbar_arrow'])

#         # Notebook (Tab) style
#         style.configure("TNotebook", background=theme['bg'])
#         style.configure("TNotebook.Tab", 
#                         background=theme['tab_bg'], 
#                         foreground=theme['tab_fg'], 
#                         padding=(10, 5))
#         style.map("TNotebook.Tab", 
#                 background=[("selected", theme['tab_selected_bg'])], 
#                 foreground=[("selected", theme['tab_selected_fg'])])

#         # Configure Tooltips (if you are using custom tooltips)
#         style.configure("TToolTip", background=theme['tooltip_bg'], foreground=theme['tooltip_fg'], relief="solid")