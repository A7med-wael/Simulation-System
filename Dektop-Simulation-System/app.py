import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from typing import Dict, Any
import os
from ThemeManager import ThemeManager
import ttkbootstrap as ttkboot
from ttkbootstrap.constants import *
from datetime import timedelta

class QueuingSystemGUI:
    def __init__(self, root: tk.Tk) -> None:
        """Initialize the Queuing System GUI."""
        self.root = root
        self.root.title("Simulation System")
        self.root.geometry("1200x800")
        
        self.simulation_type = "single" 

        # Initialize theme state
        self.is_dark_mode = False
        self.colors = {
            "bg": "#1E1E1E",  
            "fg": "#FFFFFF",   
            "entry_bg": "#2D2D2D",  
            "button_bg": "#3C3C3C",  
            "accent": "#007ACC"  
        }
        
        self.arrival_data = []
        self.server_data = {1: [], 2: []}
        # Create theme switch before other components
        self.create_theme_switch()
        
        # Configure initial style
        self.setup_style()
        
        # Initialize data structures
        self.initialize_data()
        
        # Create main container
        self.main_container = ttk.Frame(self.root, style="Custom.TFrame")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.show_probability_columns = False
        self.control_panel_visible = False
        self.data_visible = True
        
        # Setup GUI components
        self.setup_gui()
        
        # Initially hide the data frames and show logo
        self.create_data_frames()
        self.show_data_frames()
        # Apply initial theme
        self.apply_theme()

    def create_theme_switch(self) -> None:
        """Create the theme switch button."""
        # Create a frame for the switch
        self.switch_frame = ttk.Frame(self.root)
        self.switch_frame.pack(side="top", anchor="ne", padx=10, pady=5)
        
        # Create switch button
        self.theme_switch = ttk.Button(
            self.switch_frame,
            text="🌙" if not self.is_dark_mode else "☀️",
            command=self.toggle_theme,
            width=3
        )
        self.theme_switch.pack(side="right")
        
        # Create tooltip
        self.create_tooltip(self.theme_switch, "Toggle Dark/Light Mode")

    def clear_all_data(self) -> None:
        """Clear all current data and reset displays."""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all data?"):
            try:
                self.current_data = pd.DataFrame(columns=[
                    'Customer ID', 'Event Type', 'Clock Time', 'Service Code', 
                    'Service Title', 'Service Duration', 'End Time'
                ])
                
                # Hide data frames and show logo
                self.hide_data_frames()
                self.data_visible = False
                
                messagebox.showinfo("Success", "All data cleared successfully!")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear data: {str(e)}") 

    def setup_style(self) -> None:
        """Configure the application style to apply dark or light theme consistently across all widgets."""
        # Initialize style based on dark mode
        theme_name = "darkly" if self.is_dark_mode else "flatly"  # Choose dark or light theme
        style = ttkboot.Style(theme_name)

        # Get theme colors from ttkbootstrap directly
        theme = ThemeManager.get_theme(self.is_dark_mode)

        # Frame styles with enhanced label styling
        style.configure("TFrame", background=theme['bg'])
        
        # Configure both the frame and its label for dark mode
        style.configure("TLabelFrame", 
                    background=theme['bg'], 
                    foreground=theme['fg'], 
                    padding=10,
                    bordercolor=theme.get('border', theme['fg']),  
                    darkcolor=theme['bg'],  
                    lightcolor=theme['bg'])  
        
        style.configure("TLabelframe.Label", 
                    background=theme['bg'], 
                    foreground=theme['fg'],
                    font=("Helvetica", 10, "bold"))  
        
        # Configure the border color for the label frame
        style.map("TLabelframe", 
                background=[("active", theme['bg']), ("disabled", theme['bg'])],
                foreground=[("active", theme['fg']), ("disabled", theme['fg'])])

        # Label style
        style.configure("TLabel", background=theme['bg'], foreground=theme['fg'])

        # Entry style
        style.configure("TEntry", fieldbackground=theme['entry_bg'], foreground=theme['fg'], background=theme['entry_bg'])

        # Button style - leverage ttkbootstrap styles for dark theme buttons
        style.configure("TButton", bootstyle="primary" if self.is_dark_mode else "secondary", padding=5)
        style.configure("ControlFrame.TButton", bootstyle="primary" if self.is_dark_mode else "secondary", padding=5)

        # Toggle Button style
        style.configure("Toggle.TButton", bootstyle="info-outline", padding=5, width=3)

        # Treeview style
        style.configure("Treeview", background=theme['bg'], fieldbackground=theme['bg'], foreground=theme['fg'])
        style.map("Treeview", background=[("selected", theme['selected_bg'])], foreground=[("selected", theme['selected_fg'])])
        style.configure("Treeview.Heading", background=theme['header_bg'], foreground=theme['header_fg'], font=("Helvetica", 10, "bold"))

        # Scrollbar style
        style.configure("Vertical.TScrollbar", background=theme['scrollbar_bg'], troughcolor=theme['scrollbar_trough'], arrowcolor=theme['scrollbar_arrow'])
        style.configure("Horizontal.TScrollbar", background=theme['scrollbar_bg'], troughcolor=theme['scrollbar_trough'], arrowcolor=theme['scrollbar_arrow'])

        # Notebook (Tab) style
        style.configure("TNotebook", background=theme['bg'])
        style.configure("Vertical.TNotebook", background=theme['bg'])  # Specific for sidebar notebook
        style.configure("Vertical.TNotebook.Tab", background=theme['bg'], foreground=theme['fg'], padding=(5, 5), width=20)
        style.map("Vertical.TNotebook.Tab", 
              background=[("selected", theme['selected_bg']), ("!selected", theme['bg'])],
              foreground=[("selected", theme['selected_fg']), ("!selected", theme['fg'])])

        # Store tooltip colors as instance variables
        self.tooltip_bg = theme.get('tooltip_bg', theme['bg'])
        self.tooltip_fg = theme.get('tooltip_fg', theme['fg'])

    def setup_gui(self) -> None:
        """Setup the main GUI components with VSCode-like layout."""
        self.setup_style()
        
        # Create main container
        self.main_container.pack(fill="both", expand=True)

        theme = ThemeManager.get_theme(self.is_dark_mode)

        # Create the left sidebar notebook
        self.sidebar = ttk.Notebook(self.main_container, style="Vertical.TNotebook")
        self.sidebar.pack(side="left", fill="y", expand=False)

        # Track the state of each tab
        self.tab_states = {
            'control': False,
            'service': False,
            'parallel': False
        }
        
        # Store the currently open tab (None if no tab is open)
        self.current_tab = None

        # Configure style for VSCode-like appearance
        style = ttk.Style()
        style.configure(
            "Vertical.TNotebook", 
            background=theme['bg'],
            borderwidth=0,
            tabposition="wn",
            padding=0
        )
        style.configure(
            "Vertical.TNotebook.Tab",
            padding=[10, 10], 
            background=theme['bg'],
            foreground=theme['fg'],
            width=5,
            anchor="center",
            borderwidth=0
        )
        style.map("Vertical.TNotebook.Tab",
            background=[
                ("selected", theme['selected_bg']),
                ("!selected", theme['bg']),
                ("active", theme['selected_bg']),
                ("disabled", theme['bg'])
            ],
            foreground=[
                ("selected", theme['selected_fg']),
                ("!selected", theme['fg']),
                ("active", theme['selected_fg']),
                ("disabled", theme['fg'])
            ]
        )

        # Apply the vertical style to the notebook
        self.sidebar.configure(style="Vertical.TNotebook")

        # Create container frames for each tab
        self.control_container = ttk.Frame(self.sidebar)
        self.service_container = ttk.Frame(self.sidebar)
        self.parallel_container = ttk.Frame(self.sidebar)

        # Create content frames
        self.control_content = ttk.Frame(self.control_container)
        self.service_content = ttk.Frame(self.service_container)
        self.parallel_content = ttk.Frame(self.parallel_container)

        # Add container frames to notebook with icons
        self.sidebar.add(self.control_container, text="⚙️")
        self.sidebar.add(self.service_container, text="🔧")
        self.sidebar.add(self.parallel_container, text="📊")

        # Set up tooltip texts for the tabs
        self.create_tooltip(self.control_container, "Controls")
        self.create_tooltip(self.service_container, "Services")
        self.create_tooltip(self.parallel_container, "Parallel Server Data")

        # Create the right panel and other components
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.right_panel = ttk.Frame(self.content_frame)
        self.right_panel.pack(side="right", fill="both", expand=True)

        # Initialize tab contents
        self.create_control_frame(self.control_content)
        self.create_service_form(self.service_content)
        self.create_Parallel_simulation_form(self.parallel_content)

        # Create data frames
        self.create_data_frames()

        # Bind the tab change event to our custom handler
        self.sidebar.bind("<Button-1>", self.handle_tab_click, add="+")

    def get_clicked_tab(self, event):
        """Determine which tab was clicked based on click coordinates."""
        try:
            clicked_tab = self.sidebar.index(f"@{event.x},{event.y}")
            tab_mapping = {
                0: 'control',
                1: 'service',
                2: 'parallel'
            }
            return clicked_tab, tab_mapping.get(clicked_tab)
        except tk.TclError:  # Click was not on a tab
            return None, None

    def handle_tab_click(self, event):
        """Handle tab clicks with toggle behavior."""
        clicked_tab_index, tab_name = self.get_clicked_tab(event)
        
        if clicked_tab_index is None or tab_name is None:
            return
        
        # Get the content frame for the clicked tab
        content_frames = {
            'control': self.control_content,
            'service': self.service_content,
            'parallel': self.parallel_content
        }
        content_frame = content_frames[tab_name]

        # If clicking the currently open tab, close it
        if self.current_tab == tab_name:
            # Hide the content
            content_frame.pack_forget()
            # Reset the tab state
            self.tab_states[tab_name] = False
            self.current_tab = None
            # Collapse the sidebar
            self.sidebar.configure(width=1)
            return

        # If a different tab was open, close it
        if self.current_tab is not None:
            old_content = content_frames[self.current_tab]
            old_content.pack_forget()
            self.tab_states[self.current_tab] = False

        # Open the clicked tab
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.tab_states[tab_name] = True
        self.current_tab = tab_name
        self.sidebar.configure(width=300)  # Expand sidebar

    def show_tab_contents(self, tab_name):
        """Show contents of a specific tab."""
        content_frames = {
            'control': self.control_content,
            'service': self.service_content,
            'parallel': self.parallel_content
        }
        content_frames[tab_name].pack(fill="both", expand=True, padx=5, pady=5)
        self.sidebar.configure(width=300)

    def hide_tab_contents(self, tab_name):
        """Hide contents of a specific tab."""
        content_frames = {
            'control': self.control_content,
            'service': self.service_content,
            'parallel': self.parallel_content
        }
        content_frames[tab_name].pack_forget()

    def apply_theme(self) -> None:
        """Apply the current theme to all components."""
        theme = ThemeManager.get_theme(self.is_dark_mode)
        
        # Configure ttk styles
        style = ttk.Style()
        style.configure("TFrame", background=theme['bg'])
        style.configure("TLabelframe", background=theme['bg'], foreground=theme['fg'])
        style.configure("TLabel", background=theme['bg'], foreground=theme['fg'])
        style.configure("TButton", background=theme['button_bg'], foreground=theme['button_fg'])
        style.configure("Treeview", 
                       background=theme['tree_bg'], 
                       foreground=theme['tree_fg'],
                       fieldbackground=theme['tree_bg'])
        style.configure("TEntry", 
                       fieldbackground=theme['entry_bg'], 
                       foreground=theme['entry_fg'])
        
        # Update the root window
        self.root.configure(bg=theme['bg'])
        
        # Update main container
        if hasattr(self, 'main_container'):
            self.main_container.configure(style="Custom.TFrame")
        
        # Update graph if it exists
        if hasattr(self, 'figure'):
            self.figure.set_facecolor(theme['graph_bg'])
            if hasattr(self, 'ax'):
                self.ax.set_facecolor(theme['graph_bg'])
                self.ax.tick_params(colors=theme['graph_fg'])
                self.ax.xaxis.label.set_color(theme['graph_fg'])
                self.ax.yaxis.label.set_color(theme['graph_fg'])
                self.ax.title.set_color(theme['graph_fg'])
                self.ax.grid(True, linestyle='--', alpha=0.7, color=theme['grid_color'])
                
                if hasattr(self, 'canvas'):
                    self.canvas.draw()
        
        # Update all frames
        for widget in self.root.winfo_children():
            if isinstance(widget, (ttk.Frame, ttk.LabelFrame)):
                widget.configure(style="Custom.TFrame")
        
        # Force redraw of the interface
        self.root.update_idletasks()

    def hide_data_frames(self) -> None:
        """Hide all data frames."""
        if hasattr(self, 'tables_container'):
            self.tables_container.pack_forget()
        if hasattr(self, 'graph_frame'):
            self.graph_frame.pack_forget()

    def show_data_frames(self) -> None:
        """Show all data frames and hide logo, ensuring no duplicates."""
        # Hide empty state if it exists and is visible
        if hasattr(self, 'empty_state_frame') and self.empty_state_frame.winfo_ismapped():
            self.empty_state_frame.pack_forget()
        
        # Ensure tables_container is packed if not already packed
        if not self.tables_container.winfo_ismapped():
            self.tables_container.pack(fill="both", expand=True, pady=(0, 5))
        
        if hasattr(self, 'tables_container'):
            self.tables_container.pack(fill="both", expand=True, pady=5)

        # Ensure graph frame is packed if not already packed
        if hasattr(self, 'graph_frame') and not self.graph_frame.winfo_ismapped():
            self.graph_frame.pack(fill="both", expand=True)
        
        self.data_visible = True

    def create_data_frames(self) -> None:
        """Create all data frames for both single and parallel server simulations."""
        
        # Create containers only if they don't exist
        if not hasattr(self, 'tables_container'):
            # Main container for all tables
            self.tables_container = ttk.Frame(self.right_panel)
            
            # Create notebook for managing different views
            self.table_notebook = ttk.Notebook(self.tables_container)
            
            # Single Server View
            self.single_server_frame = ttk.Frame(self.table_notebook)
            
            # Create Customer Data frame for single server
            self.data_frame = ttk.LabelFrame(self.single_server_frame, text="Customer Data", padding="10")
            self.create_data_frame(self.data_frame)
            self.data_frame.pack(fill="both", expand=True, side="top", pady=(0, 5))
            
            # Create Chronological Order frame for single server
            self.chrono_frame = ttk.LabelFrame(self.single_server_frame, text="Chronological Order of Events", padding="10")
            self.create_chronological_table(self.chrono_frame)
            self.chrono_frame.pack(fill="both", expand=True, side="bottom", pady=5)
            
            # Parallel Servers View
            self.parallel_server_frame = ttk.Frame(self.table_notebook)
            
            # Create Parallel Servers Data frame
            self.parallel_data_frame = ttk.LabelFrame(self.parallel_server_frame, text="Parallel Servers Simulation Data", padding="10")
            self.create_parallel_data_frame(self.parallel_data_frame)
            self.parallel_data_frame.pack(fill="both", expand=True, pady=5)
            
            # Add frames to notebook
            self.table_notebook.add(self.single_server_frame, text="Single Server View")
            self.table_notebook.add(self.parallel_server_frame, text="Parallel Servers View")
            
            # Pack the notebook
            self.table_notebook.pack(fill="both", expand=True)
            
        # Create graph frame if it doesn't exist
        if not hasattr(self, 'graph_frame'):
            self.graph_frame = ttk.LabelFrame(self.right_panel, text="System State Graph", padding="10")
            self.create_graph_frame(self.graph_frame)
        
        # Create function to switch views based on simulation type
        def switch_view(simulation_type: str) -> None:
            """Switch between single and parallel server views."""
            if simulation_type == "parallel":
                self.table_notebook.select(1)  # Select parallel servers tab
                if hasattr(self, 'current_data') and not self.current_data.empty:
                    self.update_tree()
                    self.update_graph_multi_servers()
            else:
                self.table_notebook.select(0)  # Select single server tab
                if hasattr(self, 'current_data') and not self.current_data.empty:
                    self.update_parallel_tree()
                    self.update_graph_multi_servers()
                else:
                    self.update_tree()
                    self.update_chronological_table()
                    self.update_graph_single_server()
        
        # Store the switch_view function as an instance method
        self.switch_simulation_view = switch_view

    def toggle_theme(self) -> None:
        """Toggle between light and dark themes."""
        self.is_dark_mode = not self.is_dark_mode
        self.theme_switch.configure(text="☀️" if self.is_dark_mode else "🌙")
        self.apply_theme()

    def initialize_data(self) -> None:
        """Initialize data structures."""
        self.data_file_path = "queuing_data.xlsx"
        self.current_data = pd.DataFrame(columns=[
            'Customer ID', 'Event Type', 'Clock Time', 
            'Service Code', 'Service Title', 'Service Duration', 'End Time'
        ])
        self.services: Dict[str, Dict[str, Any]] = {}

    def create_control_frame(self, parent: ttk.Frame) -> None:
        """Create the control buttons frame with VSCode-like styling."""
        control_frame = ttk.Frame(parent, padding="10", style="Custom.TFrame")
        control_frame.pack(fill="both", expand=True)
        
        btn_configs = [
            ("Upload Data", self.upload_file, "Upload service data from file"),
            ("Probability Simulation", self.probability_simulation, "Run probability simulation"),
            ("Simulate", self.generate_customers, "Generate new customer data"),
            ("Save All", self.save_all_data, "Save current simulation data"),
            ("Clear All", self.clear_all_data, "Clear all current data")
        ]
        
        for text, command, tooltip in btn_configs:
            btn = ttk.Button(
                control_frame,
                text=text,
                command=command,
                width=20,
                style="ControlFrame.TButton"
            )
            btn.pack(pady=2)
            self.create_tooltip(btn, tooltip)

    def create_tooltip(self, widget: ttk.Widget, text: str) -> None:
        """Create a tooltip for a widget."""
        def enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

            label = ttk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
            label.pack()

            widget.tooltip = tooltip

        def leave(event):
            if hasattr(widget, "tooltip"):
                widget.tooltip.destroy()
                delattr(widget, "tooltip")

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    
    def create_service_form(self, parent: ttk.Frame) -> None:
        """Create the service input form with VSCode-like styling."""
        
        # Main frame for form with padding and style
        form_frame = ttk.Frame(parent, padding="10", style="Custom.TFrame")
        form_frame.pack(fill="both", expand=True)
        
        # Label frame to contain the form fields
        form_label = ttk.LabelFrame(form_frame, text="Service Form", padding="10", style="Custom.TLabelframe")
        form_label.pack(fill="x", pady=(0, 10))

        # Field configurations
        fields = [
            ("Service Code:", "service_code_entry"),
            ("Service Title:", "service_title_entry"),
            ("Duration (min):", "service_duration_entry")
        ]

        # Loop to create each field with label and entry
        for label_text, entry_name in fields:
            container = ttk.Frame(form_label, style="Custom.TFrame")  # Use form_label as parent
            container.pack(fill="x", pady=5)
            
            # Label for field
            label = ttk.Label(container, text=label_text, style="Custom.TLabel")
            label.pack(side="left", padx=(0, 5))
            
            # Entry for field
            entry = ttk.Entry(container, style="Custom.TEntry", width=30)
            entry.pack(side="right", fill="x", expand=True, padx=(5, 0))
            
            # Bind the entry to the self object
            setattr(self, entry_name, entry)

        # Add Service Button
        add_btn = ttk.Button(
            form_frame,
            text="Add Service",
            command=self.add_service,
            width=15,
            style="ControlFrame.TButton"
        )
        add_btn.pack(pady=10)  # Adjusted padding for button

    def create_data_frame(self, parent: ttk.Frame) -> None:
        """Create the main data display treeview directly in the parent frame."""
        columns = ("Customer ID", "Event Type", "Clock Time", "Service Code", 
                "Service Title", "Service Duration", "End Time")
        
        # Create Treeview in the provided parent frame
        self.tree = ttk.Treeview(parent, columns=columns, show="headings")

        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Add scrollbars
        self.add_scrollbars(parent, self.tree)
        
        # Pack the Treeview
        self.tree.pack(fill="both", expand=True)

    def create_parallel_data_frame(self, parent: ttk.Frame) -> None:
        """Create the parallel servers data display treeview."""
        columns = (
            "Customer ID", "Server", "Arrival Time", "Wait Time",
            "Service Start", "Service Duration", "Service End",
            "System Time"
        )
        self.parallel_tree = ttk.Treeview(parent, columns=columns, show="headings")

        for col in columns:
            self.parallel_tree.heading(col, text=col)
            self.parallel_tree.column(col, width=150)

        
        self.add_scrollbars(parent, self.parallel_tree)        
        self.parallel_tree.pack(fill="both", expand=True)

    def create_chronological_table(self, parent: ttk.Frame) -> None:
        """Create the chronological events table directly in the parent frame."""
        
        columns = ("Time", "Event Type", "Customer ID", "Service")
        self.chrono_tree = ttk.Treeview(parent, columns=columns, show="headings", height=5)

        # Configure columns with specific widths
        column_widths = {"Time": 100, "Event Type": 100, "Customer ID": 100, "Service": 200}
        for col, width in column_widths.items():
            self.chrono_tree.heading(col, text=col)
            self.chrono_tree.column(col, width=width)

        # Add scrollbars
        self.add_scrollbars(parent, self.chrono_tree)

        # Pack the Treeview
        self.chrono_tree.pack(fill="both", expand=True, pady=5)

    def create_graph_frame(self, parent: ttk.Frame) -> None:
        """Create the graph display frame."""
        try:
            if hasattr(self, 'figure') and self.figure is not None:
                plt.close(self.figure)

            # Create figure and axis with a specific size
            self.figure, self.ax = plt.subplots(figsize=(10, 4), dpi=100)
            theme = ThemeManager.get_theme(self.is_dark_mode)
            self.figure.set_facecolor(theme['graph_bg'])
            self.ax.set_facecolor(theme['graph_bg'])

            # Create canvas and pack it
            self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
            
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
            

            # Initialize empty graph if no data is available
            if not hasattr(self, 'current_data') or self.current_data.empty:
                self._show_empty_graph()
            else:
                self.update_graph_single_server()

        except Exception as e:
            print(f"Error creating graph frame: {str(e)}")
            messagebox.showerror("Error", f"Failed to create graph frame: {str(e)}")

    def add_scrollbars(self, parent: ttk.Frame, widget: ttk.Treeview) -> None:
        """Add scrollbars to a widget."""
        y_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=widget.yview)
        x_scrollbar = ttk.Scrollbar(parent, orient="horizontal", command=widget.xview)
        widget.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        x_scrollbar.pack(side="bottom", fill="x")
        y_scrollbar.pack(side="right", fill="y")
        widget.pack(side="left", fill="both", expand=True)

    def add_service(self) -> None:
        """Add a new service to the system."""
        try:
            code = self.service_code_entry.get().strip()
            title = self.service_title_entry.get().strip()
            duration = self.service_duration_entry.get().strip()

            if not all([code, title, duration]):
                raise ValueError("Please fill all fields.")

            duration = int(duration)
            if duration <= 0:
                raise ValueError("Duration must be a positive number.")

            if code in self.services:
                raise ValueError(f"Service code '{code}' already exists.")

            self.services[code] = {'title': title, 'duration': duration}
            messagebox.showinfo("Success", f"Service {title} added successfully!")
            
            # Clear entries
            for entry in [self.service_code_entry, self.service_title_entry, self.service_duration_entry]:
                entry.delete(0, 'end')

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def generate_customers(self) -> None:
        """Generate random customer data without service overlap tracking."""
        # Basic validation
        if not self.services:
            messagebox.showerror("Error", "No services available! Please add services first.")
            return

        try:
            self.show_probability_columns = False  # Ensure no probability columns for normal simulation
            
            # Generate customers
            num_customers = random.randint(5, 10)
            arrival_time = 0
            new_data = []

            for customer_id in range(1, num_customers + 1):
                # Calculate arrival and service times
                interval = random.randint(1, 3)
                arrival_time += interval
                
                # Select random service
                service_code = random.choice(list(self.services.keys()))
                service_info = self.services[service_code]
                service_duration = service_info['duration']
                departure_time = arrival_time + service_duration
                
                # Generate arrival and departure events
                for event_type in ['Arrival', 'Departure']:
                    event_time = arrival_time if event_type == 'Arrival' else departure_time
                    new_data.append({
                        'Customer ID': customer_id,
                        'Event Type': event_type,
                        'Clock Time': event_time,
                        'Service Code': service_code,
                        'Service Title': service_info['title'],
                        'Service Duration': service_duration,
                        'End Time': departure_time
                    })

            # Update the DataFrame
            self.current_data = pd.DataFrame(new_data)

            self.show_data_frames()
            self.update_displays()
            
            messagebox.showinfo("Simulation Complete", "Simulation completed successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate customers: {str(e)}")

    def probability_simulation(self) -> None:
        """Run a probability-based simulation for customer events and display probability columns."""
        if not self.services:
            messagebox.showerror("Error", "No services available! Please add services first.")
            return

        try:
            arrival_probability = 0.6  # 60% chance of customer arrival per time unit
            service_completion_probability = 0.8
            max_customers = 20
            simulated_data = []
            arrival_time = 0

            for customer_id in range(1, max_customers + 1):
                if random.random() <= arrival_probability:
                    arrival_time += random.randint(1, 3)

                    service_code = random.choice(list(self.services.keys()))
                    service_info = self.services[service_code]
                    service_duration = service_info['duration']
                    departure_time = arrival_time + service_duration

                    # Probability-based columns
                    arrival_prob = round(random.random(), 2)
                    completion_prob = round(service_completion_probability, 2)

                    simulated_data.append({
                        'Customer ID': customer_id,
                        'Event Type': 'Arrival',
                        'Clock Time': arrival_time,
                        'Service Code': service_code,
                        'Service Title': service_info['title'],
                        'Service Duration': service_duration,
                        'End Time': departure_time,
                        'Arrival Probability': arrival_prob,
                        'Completion Probability': completion_prob
                    })
                    simulated_data.append({
                        'Customer ID': customer_id,
                        'Event Type': 'Departure',
                        'Clock Time': departure_time,
                        'Service Code': service_code,
                        'Service Title': service_info['title'],
                        'Service Duration': service_duration,
                        'End Time': departure_time,
                        'Arrival Probability': arrival_prob,
                        'Completion Probability': completion_prob
                    })

            # Update the DataFrame
            self.current_data = pd.DataFrame(simulated_data)
            
            # Set flag to show probability columns
            self.show_probability_columns = True
                
            # Show data frames
            self.show_data_frames()
            
            # Update displays
            self.update_displays()
            messagebox.showinfo("Probability Simulation Complete", "Probability-based simulation completed successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to run probability simulation: {str(e)}")

    def create_Parallel_simulation_form(self, parent: ttk.Frame) -> None:
        """Create the simulation setup form in the existing tab."""
        # Main container
        form_frame = ttk.Frame(parent, padding="10")
        form_frame.pack(fill="both", expand=True)
        
        # Data Import/Export Section
        upload_frame = ttk.LabelFrame(form_frame, text="Data Import/Export", padding=10)
        upload_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(upload_frame, text="Upload", command=self.upload_Parallel_Server_file).pack(side="left", padx=5)
        ttk.Button(upload_frame, text="Save", command=self.save_Parellel_server_data).pack(side="left", padx=5)
        ttk.Button(upload_frame, text="Simulate", command=self.run_parallel_simulation).pack(side="left", padx=5)

        # Arrival Probability Input Section
        arrival_frame = ttk.LabelFrame(form_frame, text="Arrival Probability", padding=10)
        arrival_frame.pack(fill="x", pady=(10, 10))

        arrival_fields = [
            ("Time Between Arrivals:", "time_between_arrivals_entry"),
            ("Probability:", "probability_entry"),
            ("Accumulative Probability:", "accum_probability_entry"),
            ("Digit Assignment From:", "digit_assignment_from_entry"),
            ("Digit Assignment To:", "digit_assignment_to_entry"),
        ]
        
        self.arrival_entries = {}
        for label_text, entry_name in arrival_fields:
            row_frame = ttk.Frame(arrival_frame)
            row_frame.pack(fill="x", pady=2)
            
            ttk.Label(row_frame, text=label_text).pack(side="left")
            
            entry = ttk.Entry(row_frame, width=15)
            entry.pack(side="right", padx=(5, 0), fill="x", expand=True)
            self.arrival_entries[entry_name] = entry

        # Add button to add arrival data
        ttk.Button(arrival_frame, text="Add Arrival Data", command=self.add_arrival_data).pack(pady=10)

        # Arrival TreeView for displaying added arrival data
        self.arrival_tree = ttk.Treeview(arrival_frame, columns=[
            "Time Between Arrivals", "Probability", "Accumulative Probability", 
            "Digit Assignment From", "Digit Assignment To"
        ], show="headings", height=5)
        for col in self.arrival_tree["columns"]:
            self.arrival_tree.heading(col, text=col)
            self.arrival_tree.column(col, width=120)

        self.arrival_tree.pack(fill="x", pady=(10, 10))

        # Server Data Section
        server_frame = ttk.LabelFrame(form_frame, text="Server Data", padding=10)
        server_frame.pack(fill="x", pady=(10, 10))

        ttk.Label(server_frame, text="Server No:").pack(anchor="w", pady=(0, 5))
        self.server_var = tk.StringVar(value="1")
        self.server_combo = ttk.Combobox(
            server_frame, textvariable=self.server_var, values=["1", "2"], state="readonly", width=5
        )
        self.server_combo.pack(anchor="w", pady=(0, 10))

        # Server data input fields
        server_fields = [
            ("Service Time:", "service_time_entry"),
            ("Probability:", "service_probability_entry"),
            ("Accumulative Probability:", "service_accum_probability_entry"),
            ("Digit Assignment From:", "service_digit_assignment_from_entry"),
            ("Digit Assignment To:", "service_digit_assignment_to_entry"),
        ]
        
        self.server_entries = {}
        for label_text, entry_name in server_fields:
            row_frame = ttk.Frame(server_frame)
            row_frame.pack(fill="x", pady=2)
            
            ttk.Label(row_frame, text=label_text).pack(side="left")
            
            entry = ttk.Entry(row_frame, width=15)
            entry.pack(side="right", padx=(5, 0), fill="x", expand=True)
            self.server_entries[entry_name] = entry

        # Add button to add server data
        ttk.Button(server_frame, text="Add Server Data", command=self.add_server_data).pack(pady=10)

        # Server TreeView for displaying added server data
        self.server_tree = ttk.Treeview(server_frame, columns=[
            "Service Time", "Probability", "Accumulative Probability", 
            "Digit Assignment From", "Digit Assignment To"
        ], show="headings", height=5)
        for col in self.server_tree["columns"]:
            self.server_tree.heading(col, text=col)
            self.server_tree.column(col, width=120)

        self.server_tree.pack(fill="x", pady=(10, 10))

    def add_arrival_data(self) -> None:
        """Add arrival probability data to the arrival tree."""
        try:
            data = [self.arrival_entries[field].get() for field in self.arrival_entries]
            if not all(data):
                raise ValueError("All fields must be filled")

            # Validate numeric values
            for i, value in enumerate(data[1:]):  # Skip the first field if it's text
                try:
                    float(value)
                except ValueError:
                    raise ValueError(f"Invalid numeric value in {self.arrival_tree['columns'][i+1]}")

            self.arrival_tree.insert("", "end", values=data)

            # Clear entry fields
            for entry in self.arrival_entries.values():
                entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_server_data(self) -> None:
        """Add server probability data to the server tree."""
        try:
            data = [self.server_entries[field].get() for field in self.server_entries]
            if not all(data):
                raise ValueError("All fields must be filled")

            # Validate numeric values
            for i, value in enumerate(data[1:]):  # Skip the first field if it's text
                try:
                    float(value)
                except ValueError:
                    raise ValueError(f"Invalid numeric value in {self.server_tree['columns'][i+1]}")

            self.server_tree.insert("", "end", values=data)

            # Clear entry fields
            for entry in self.server_entries.values():
                entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def upload_Parallel_Server_file(self) -> None:
        """Upload probability data from Excel file."""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
            
            if not file_path:
                return

            df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            
            # Clear existing data
            for item in self.arrival_tree.get_children():
                self.arrival_tree.delete(item)
            for item in self.server_tree.get_children():
                self.server_tree.delete(item)

            # Process arrival probability data
            arrival_cols = list(self.arrival_entries.keys())
            if all(col in df.columns for col in arrival_cols):
                arrival_data = df[arrival_cols].values.tolist()
                for row in arrival_data:
                    if not pd.isna(row).any():  # Skip rows with missing values
                        self.arrival_tree.insert("", "end", values=row)
                self.arrival_data = arrival_data

            # Process server data
            server_cols = list(self.server_entries.keys())
            if all(col in df.columns for col in server_cols):
                server_data = df[server_cols].values.tolist()
                for row in server_data:
                    if not pd.isna(row).any():  # Skip rows with missing values
                        self.server_tree.insert("", "end", values=row)
                    self.server_data[int(self.server_var.get())] = server_data

            messagebox.showinfo("Success", "Data uploaded successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload data: {str(e)}")

    def save_Parellel_server_data(self) -> None:
        """Save probability data to Excel file."""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
            
            if not file_path:
                return

            # Create DataFrames for arrival and server data
            arrival_df = pd.DataFrame(self.arrival_data, columns=list(self.arrival_entries.keys()))
            server_df = pd.DataFrame(self.server_data[int(self.server_var.get())], 
                                columns=list(self.server_entries.keys()))

            # Save to Excel with multiple sheets
            with pd.ExcelWriter(file_path) as writer:
                arrival_df.to_excel(writer, sheet_name='Arrival Probability', index=False)
                server_df.to_excel(writer, sheet_name=f'Server-{self.server_var.get()}', index=False)

            messagebox.showinfo("Success", "Data saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

    def run_parallel_simulation(self) -> None:
        """Run the parallel server simulation."""
        try:
            self.simulation_type = "parallel" 
            self.update_displays()
            # Collect and convert data from trees
            arrival_data = [
                {
                    'Time Between Arrivals': int(item[0]),
                    'Probability': float(item[1]),
                    'Cumulative Probability': float(item[2]),
                    'Digit Assignment From': int(item[3]),
                    'Digit Assignment To': int(item[4])
                }
                for item in (self.arrival_tree.item(child)["values"] for child in self.arrival_tree.get_children())
            ]

            server_data = [
                {
                    'Service Time': int(item[0]),
                    'Probability': float(item[1]),
                    'Cumulative Probability': float(item[2]),
                    'Digit Assignment From': int(item[3]),
                    'Digit Assignment To': int(item[4])
                }
                for item in (self.server_tree.item(child)["values"] for child in self.server_tree.get_children())
            ]

            if not all([arrival_data, server_data]):
                raise ValueError("Please ensure all probability tables have data")

            # Simulation parameters
            simulation_period = timedelta(hours=1)
            servers = {'Able': {'available_from': timedelta(0), 'service_times': []},
                    'Baker': {'available_from': timedelta(0), 'service_times': []}}

            customers = []
            arrival_time = timedelta(0)

            def get_time_from_probability_table(random_value, probability_table, key_name):
                for row in probability_table:
                    if random_value <= row['Cumulative Probability']:
                        return row[key_name]
                raise ValueError(f"No matching entry found in the probability table for random value: {random_value}")

            # Run simulation for each customer
            while arrival_time < simulation_period:
                random_value = random.random()
                time_between_arrivals = get_time_from_probability_table(random_value, arrival_data, 'Time Between Arrivals')
                arrival_time += timedelta(minutes=time_between_arrivals)

                if servers['Able']['available_from'] <= arrival_time:
                    assigned_server = 'Able'
                elif servers['Baker']['available_from'] <= arrival_time:
                    assigned_server = 'Baker'
                else:
                    assigned_server = 'Able' if servers['Able']['available_from'] < servers['Baker']['available_from'] else 'Baker'

                random_value = random.random()
                service_time = get_time_from_probability_table(random_value, server_data, 'Service Time')

                start_time = max(arrival_time, servers[assigned_server]['available_from'])
                end_time = start_time + timedelta(minutes=service_time)

                # Modified customer info to match the graph function's expected format
                customer_info = {
                    'Customer ID': len(customers) + 1,
                    'Clock Time': arrival_time.total_seconds() / 60,  # Convert to minutes
                    'Event Type': 'Arrival',
                    'Service Duration': service_time,
                    'End Time': end_time.total_seconds() / 60,  # Convert to minutes
                    'Server': assigned_server,
                    'Wait Time': (start_time - arrival_time).total_seconds() / 60,
                    'Service Time': service_time
                }
                customers.append(customer_info)

                servers[assigned_server]['available_from'] = end_time
                servers[assigned_server]['service_times'].append(service_time)

            # Create DataFrame with the modified structure
            df_customers = pd.DataFrame(customers)
            self.current_data = df_customers

            # Calculate metrics
            total_simulation_time = simulation_period.total_seconds() / 60
            able_busy_time = min(sum(servers['Able']['service_times']), total_simulation_time)
            baker_busy_time = min(sum(servers['Baker']['service_times']), total_simulation_time)

            metrics = {
                'Able Utilization Rate': f"{min(able_busy_time / total_simulation_time, 1.0):.2%}",
                'Baker Utilization Rate': f"{min(baker_busy_time / total_simulation_time, 1.0):.2%}",
                'Average Waiting Time': f"{df_customers['Wait Time'].mean():.2f} minutes",
                'Total Customers': len(customers)
            }


            self.show_data_frames()
            self.update_displays()
            metrics_text = "\n".join(f"{k}: {v}" for k, v in metrics.items())
            messagebox.showinfo("Simulation Complete", f"Simulation Results:\n\n{metrics_text}")

        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed: {str(e)}")

    def update_displays(self) -> None:
        """Update all displays with current data, optionally showing probability columns."""
        if hasattr(self, 'simulation_type') and self.simulation_type == "parallel":
            self.update_parallel_tree()
            self.update_graph_multi_servers()
        else:    
            self.update_tree()
            self.update_chronological_table()
            self.update_graph_single_server()
            
    def update_tree(self) -> None:
        """Update the main data tree view, optionally showing probability columns."""
        self.tree.delete(*self.tree.get_children())  # Clear existing data

        # Define base columns and add probability columns if the flag is set
        columns = ["Customer ID", "Event Type", "Clock Time", "Service Code", 
                "Service Title", "Service Duration", "End Time"]
        if self.show_probability_columns:
            columns.extend(["Arrival Probability", "Completion Probability"])

        # Reconfigure columns in the tree view
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        if not self.current_data.empty:
            sorted_data = self.current_data.sort_values("Clock Time")
            for _, row in sorted_data.iterrows():
                values = [row[col] for col in columns]  # Only display columns in the defined list
                self.tree.insert("", "end", values=values)

    def update_parallel_tree(self) -> None:
        """Update the parallel servers treeview with current simulation data."""
        try:
            # Clear existing items
            for item in self.parallel_tree.get_children():
                self.parallel_tree.delete(item)
                
            if hasattr(self, 'current_data') and not self.current_data.empty:
                for _, row in self.current_data.iterrows():
                    # Convert times to formatted strings
                    arrival_time = f"{row['Clock Time']:.2f}"
                    wait_time = f"{row['Wait Time']:.2f}"
                    service_start = f"{(row['Clock Time'] + row['Wait Time']):.2f}"
                    service_end = f"{row['End Time']:.2f}"
                    system_time = f"{(row['End Time'] - row['Clock Time']):.2f}"
                    
                    # Insert data into treeview
                    self.parallel_tree.insert('', 'end', values=(
                        f"Customer {row['Customer ID']}",
                        row['Server'],
                        f"{arrival_time} min",
                        f"{wait_time} min",
                        f"{service_start} min",
                        f"{row['Service Duration']} min",
                        f"{service_end} min",
                        f"{system_time} min"
                    ))
        except Exception as e:
            print(f"Error updating parallel tree: {str(e)}")
            messagebox.showerror("Error", f"Failed to update parallel servers table: {str(e)}")

    def update_chronological_table(self) -> None:
        """Update the chronological events table, optionally showing probability columns."""
        self.chrono_tree.delete(*self.chrono_tree.get_children())  # Clear existing data

        # Define base columns and add probability columns if the flag is set
        columns = ["Time", "Event Type", "Customer ID", "Service"]
        if self.show_probability_columns:
            columns.extend(["Arrival Probability", "Completion Probability"])

        # Reconfigure columns in the chronological tree view
        self.chrono_tree["columns"] = columns
        for col in columns:
            self.chrono_tree.heading(col, text=col)
            self.chrono_tree.column(col, width=150)

        if not self.current_data.empty:
            sorted_data = self.current_data.sort_values("Clock Time")
            for _, row in sorted_data.iterrows():
                values = [
                    f"Time {row['Clock Time']}",
                    row["Event Type"],
                    f"Customer {row['Customer ID']}",
                    row["Service Title"]
                ]
                if self.show_probability_columns:
                    values.extend([row["Arrival Probability"], row["Completion Probability"]])
                self.chrono_tree.insert("", "end", values=values)

    def update_graph_single_server(self) -> None:
        """Update the system state graph with theme support."""
        try:
            # Clear the current plot
            self.ax.clear()
            
            # Apply current theme
            theme = ThemeManager.get_theme(self.is_dark_mode)
            self.figure.set_facecolor(theme['graph_bg'])
            self.ax.set_facecolor(theme['graph_bg'])
            
            if not self.current_data.empty:
                try:
                    # Sort data by 'Clock Time' for ordered plotting
                    sorted_data = self.current_data.sort_values('Clock Time')

                    # Plot each client's arrival time and service duration
                    for index, row in sorted_data.iterrows():
                        arrival_time = row['Clock Time']
                        service_duration = row['Service Duration']
                        end_time = row['End Time']
                        client_id = row['Customer ID']
                        
                        # Plot arrival time
                        self.ax.plot(arrival_time, client_id, 'bo', label="Arrival Time" if index == 0 else "")
                        
                        # Plot service duration as a horizontal line
                        self.ax.hlines(client_id, arrival_time, end_time, colors='green', label="Service Duration" if index == 0 else "")
                        
                        # Plot end time
                        self.ax.plot(end_time, client_id, 'yo', label="End Time" if index == 0 else "")
                        
                        # Calculate and plot waiting time if applicable
                        if row['Event Type'] == 'Arrival' and row['Clock Time'] < end_time:
                            waiting_time = end_time - arrival_time
                            self.ax.plot([arrival_time, end_time], [client_id, client_id], 'y--', alpha=0.5, label="Waiting Time" if index == 0 else "")

                    # Configure graph
                    self._configure_graph()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update graph: {str(e)}")
            else:
                self._show_empty_graph()
            
            # Update the canvas
            self.figure.tight_layout()
            self.canvas.draw_idle()
            
        except Exception as e:
            print(f"Error updating graph: {str(e)}")
            messagebox.showerror("Error", f"Failed to update graph: {str(e)}")

    def update_graph_multi_servers(self) -> None:
        """Update the system state graph with a unified view of servers and customers."""
        try:
            if not hasattr(self, 'ax') or not hasattr(self, 'figure'):
                return
                
            self.ax.clear()
            theme = ThemeManager.get_theme(self.is_dark_mode)
            self.figure.set_facecolor(theme['graph_bg'])
            self.ax.set_facecolor(theme['graph_bg'])
            
            if hasattr(self, 'current_data') and not self.current_data.empty:
                # Create a unified timeline view
                server_positions = {'Able': 1, 'Baker': 2}
                
                # Plot server timelines
                for server, position in server_positions.items():
                    self.ax.hlines(
                        position, 0, self.current_data['End Time'].max(),
                        colors='gray', linestyles='--', alpha=0.3,
                        label=f'{server} Timeline'
                    )
                
                # Plot each customer's service period
                colors = {'Able': '#2ecc71', 'Baker': '#3498db'}
                
                for _, row in self.current_data.iterrows():
                    server_pos = server_positions[row['Server']]
                    service_start = row['Clock Time'] + row['Wait Time']
                    
                    # Arrival point
                    self.ax.scatter(row['Clock Time'], 0, color='#e74c3c', marker='o',
                                label='Arrival' if _ == 0 else "")
                    
                    # Wait time (if any)
                    if row['Wait Time'] > 0:
                        self.ax.vlines(row['Clock Time'], 0, server_pos,
                                    colors='#f1c40f', linestyles=':',
                                    label='Wait Time' if _ == 0 else "")
                    
                    # Service period
                    self.ax.hlines(server_pos, service_start, row['End Time'],
                                colors=colors[row['Server']], linewidth=6, alpha=0.7,
                                label=f'{row["Server"]} Service' if _ == 0 else "")
                    
                    # Customer labels
                    self.ax.text(row['Clock Time'], -0.2, f'C{row["Customer ID"]}',
                            fontsize=8, rotation=45, ha='right', va='top')
                
                # Customize the graph
                self.ax.set_ylim(-0.5, 2.5)
                self.ax.set_xlim(-2, self.current_data['End Time'].max() + 2)
                self.ax.set_yticks([0, 1, 2])
                self.ax.set_yticklabels(['Arrivals', 'Server Able', 'Server Baker'])
                
                self.ax.set_xlabel('Time (minutes)')
                self.ax.set_title('Parallel Servers Simulation Timeline')
                self.ax.grid(True, alpha=0.2)
                
                # Add legend with unique entries
                handles, labels = self.ax.get_legend_handles_labels()
                by_label = dict(zip(labels, handles))
                self.ax.legend(
                    by_label.values(), by_label.keys(),
                    loc='upper right', bbox_to_anchor=(1, 1)
                )
                
            else:
                self.ax.text(0.5, 0.5, 'No simulation data available',
                            ha='center', va='center',
                            color=theme.get('text_color', 'black'))
            
            self.figure.tight_layout()
            self.canvas.draw_idle()
            
        except Exception as e:
            print(f"Error updating multi-server graph: {str(e)}")
            messagebox.showerror("Error", f"Failed to update simulation graph: {str(e)}")

    def _add_graph_annotations(self, sorted_data: pd.DataFrame) -> None:
        """Add annotations to the graph."""
        try:
            for _, row in sorted_data.iterrows():
                client_id = row['Customer ID']
                arrival_time = row['Clock Time']
                service_duration = row['Service Duration']
                end_time = row['End Time']
                
                # Annotate arrival and end times with client ID
                self.ax.annotate(f"A{client_id}", (arrival_time, client_id), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8, color='blue')
                self.ax.annotate(f"E{client_id}", (end_time, client_id), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8, color='yellow')
                
        except Exception as e:
            print(f"Error adding annotations: {str(e)}")

    def _configure_graph(self) -> None:
        """Configure graph settings."""
        try:
            # Add grid
            self.ax.grid(True, linestyle='--', alpha=0.7)
            
            # Set labels and title
            self.ax.set_xlabel('Time', fontsize=10, labelpad=10)
            self.ax.set_ylabel('Client Number', fontsize=10, labelpad=10)
            self.ax.set_title('Client Arrival and Service End Times', fontsize=12, pad=20)
            
            # Set y-axis to show integer client numbers only
            self.ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
            
            # Add legend with unique labels only
            handles, labels = self.ax.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            self.ax.legend(by_label.values(), by_label.keys(), loc='upper left')
            
        except Exception as e:
            print(f"Error configuring graph: {str(e)}")

    def _show_empty_graph(self) -> None:
        """Show empty graph placeholder."""
        try:
            self.ax.clear()
            self.ax.text(
                0.5, 0.5,
                'No data to display\nRun a simulation to see the graph',
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=12,
                color='gray',
                transform=self.ax.transAxes
            )
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.set_frame_on(False)

            # Draw the empty placeholder
            self.canvas.draw_idle()

        except Exception as e:
            print(f"Error showing empty graph: {str(e)}")

    def upload_file(self) -> None:
        """Upload service data from file."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            required_columns = ['Service Code', 'Service Title', 'Service Duration (minutes)']
            
            if not all(col in df.columns for col in required_columns):
                raise ValueError(
                    "Invalid file format! Required columns: 'Service Code', 'Service Title', and 'Service Duration (minutes)'")
            self.services.clear()
            for _, row in df.iterrows():
                if not pd.isna(row['Service Code']):  # Skip empty rows
                    duration = int(row['Service Duration (minutes)'])
                    if duration <= 0:
                        raise ValueError(f"Invalid duration for service {row['Service Code']}: {duration}")
                        
                    self.services[str(row['Service Code'])] = {
                        'title': str(row['Service Title']),
                        'duration': duration
                    }
            
            if not self.services:
                raise ValueError("No valid services found in file")
                
            messagebox.showinfo("Success", f"Successfully loaded {len(self.services)} services!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def save_all_data(self) -> None:
        """Save current simulation data to file."""
        if self.current_data.empty:
            messagebox.showwarning("Warning", "No data to save!")
            return
            
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
            )
            
            if file_path:
                # Create a copy of the data for saving
                save_data = self.current_data.copy()
                
                # Sort by clock time for better readability
                save_data.sort_values('Clock Time', inplace=True)
                
                # Save based on file extension
                if file_path.endswith('.xlsx'):
                    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                        save_data.to_excel(writer, sheet_name='Queue Data', index=False)
                        
                        # Add services to a second sheet
                        services_df = pd.DataFrame([
                            {
                                'Service Code': code,
                                'Service Title': info['title'],
                                'Service Duration (minutes)': info['duration']
                            }
                            for code, info in self.services.items()
                        ])
                        services_df.to_excel(writer, sheet_name='Services', index=False)
                else:
                    save_data.to_csv(file_path, index=False)
                
                messagebox.showinfo("Success", "Data saved successfully!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

def main():
    """Main entry point for the application."""
    try:
        root = tk.Tk()
        root.title("Queuing System Simulation")
        
        # Set window minimum size
        root.minsize(1000, 600)
        
        # Set window icon (if available)
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "queue_icon.ico")
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        except Exception:
            pass  # Skip icon if not found or error occurs
        
        # Configure grid weight
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        
        # Create and run application
        app = QueuingSystemGUI(root)
        
        # Center window on screen
        window_width = 1200
        window_height = 800
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Start the application
        root.mainloop()
    
    except Exception as e:
        messagebox.showerror("Fatal Error", f"An unexpected error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()