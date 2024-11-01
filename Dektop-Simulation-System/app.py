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
from PIL import Image, ImageTk 

class QueuingSystemGUI:
    def __init__(self, root: tk.Tk) -> None:
        """Initialize the Queuing System GUI."""
        self.root = root
        self.root.title("Simulation System")
        self.root.geometry("1200x800")
        
        # Initialize theme state
        self.is_dark_mode = False
        self.colors = {
            "bg": "#1E1E1E",  
            "fg": "#FFFFFF",   
            "entry_bg": "#2D2D2D",  
            "button_bg": "#3C3C3C",  
            "accent": "#007ACC"  
        }
        
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
        self.control_panel_visible = True
        self.data_visible = False
        
        # Setup GUI components
        self.setup_gui()
        
        # Initially hide the data frames and show logo
        self.hide_data_frames()
        
        # Apply initial theme
        self.apply_theme()

    def create_empty_state(self) -> None:
        """Create the initial empty state with logo."""
        self.empty_state_frame = ttk.Frame(self.right_panel)
        
        # Create a canvas for the logo
        canvas = tk.Canvas(self.empty_state_frame, width=400, height=400, bg='#f0f0f0', highlightthickness=0)
        canvas.pack(expand=True)
        
        # Draw a simple queue logo (you can replace this with your own logo image)
        # This is a simple placeholder logo
        canvas.create_oval(150, 150, 250, 250, fill="#4a90e2", outline="")
        canvas.create_line(200, 250, 200, 300, fill="#4a90e2", width=3)
        canvas.create_line(180, 280, 220, 280, fill="#4a90e2", width=3)
        
        # Add welcome text
        canvas.create_text(200, 320, text="Welcome to Queuing System Simulation",
                         font=('Helvetica', 14, 'bold'), fill="#333")
        canvas.create_text(200, 350, 
                         text="Use the control panel on the left to get started",
                         font=('Helvetica', 12), fill="#666")
        
        self.empty_state_frame.pack(fill="both", expand=True)
        
        # Hide all data frames initially
        if hasattr(self, 'data_frame'):
            self.data_frame.pack_forget()
        if hasattr(self, 'chrono_frame'):
            self.chrono_frame.pack_forget()
        if hasattr(self, 'graph_frame'):
            self.graph_frame.pack_forget()

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
        self.sidebar.pack(side="left", fill="y", padx=(0, 0), pady=(0, 0))

        # Configure style for VSCode-like appearance
        style = ttk.Style()
        style.configure(
            "Vertical.TNotebook", 
            background=theme['bg'],
            borderwidth=0,
            tabposition="wn",  # West position for tabs
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
                ("active", theme['selected_bg']),  # Hover effect
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

        # Create frames for each tab
        self.control_tab = ttk.Frame(self.sidebar, style="TFrame")
        self.service_tab = ttk.Frame(self.sidebar, style="TFrame")
        self.toggle_tab = ttk.Frame(self.sidebar, style="TFrame")  # New toggle tab frame

        # Add frames to notebook with icons (or text)
        self.sidebar.add(self.toggle_tab, text="≡")  # Toggle tab
        self.sidebar.add(self.control_tab, text="⚙️")  # Control icon
        self.sidebar.add(self.service_tab, text="🔧")  # Service icon

        # Set up tooltip texts for the tabs
        self.create_tooltip(self.control_tab, "Controls")
        self.create_tooltip(self.service_tab, "Services")
        self.create_tooltip(self.toggle_tab, "Toggle Control Panel")  # Tooltip for toggle tab

        # Bind the toggle tab to the toggle function
        self.sidebar.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # Create the control and service frames in their respective tabs
        self.create_control_frame(self.control_tab)
        self.create_service_form(self.service_tab)

        # Right side content
        self.content_frame = ttk.Frame(self.main_container, style="TFrame")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Create the right panel
        self.right_panel = ttk.Frame(self.content_frame)
        self.right_panel.pack(side="right", fill="both", expand=True)

        # Create separate frames for the two tables
        self.customer_data_frame = ttk.Frame(self.right_panel, style="TFrame")
        self.chronological_frame = ttk.Frame(self.right_panel, style="TFrame")

        # Arrange frames within right_panel
        self.customer_data_frame.pack(side="top", fill="both", expand=True, padx=5, pady=(0, 5))
        self.chronological_frame.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

        # Create data frames
        self.create_data_frames()

    def on_tab_change(self, event) -> None:
        """Handle tab selection to toggle the control panel when the toggle tab is clicked."""
        # Get the selected tab index
        selected_tab = event.widget.index("current")

        # If the toggle tab (first tab) is selected, toggle the control panel
        if selected_tab == 0:
            self.toggle_control_panel()
   
    def toggle_control_panel(self) -> None:
        """Toggle the visibility of the control panel and adjust the main frame."""
        if self.control_panel_visible:
            # Collapse the sidebar to only show icons
            self.sidebar.pack_configure(fill="y", expand=False, side="left", padx=(0, 0))
            self.sidebar.config(width=1)  # Reduce width to show icons only

            # Hide content inside each tab to show only icons
            for child in (self.control_tab, self.service_tab):
                for widget in child.winfo_children():
                    widget.grid_remove()  # Hide widgets in each tab without removing the frame

            # Expand the main content to use more space
            self.content_frame.pack_configure(fill="both", expand=True, side="right")
        else:
            # Expand the sidebar to show full tab content
            self.sidebar.pack_configure(fill="y", expand=False, side="left")
            self.sidebar.config(width=250)  # Restore full width

            # Restore the widgets in each tab
            for child in (self.control_tab, self.service_tab):
                for widget in child.winfo_children():
                    widget.grid()  # Show widgets again when expanded

        # Toggle the flag for control panel visibility
        self.control_panel_visible = not self.control_panel_visible

        # Update toggle button text based on visibility
        self.sidebar.tab(0, text="≡" if self.control_panel_visible else "☰")

            
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
        
        # Hide logo frame if it exists and is visible
        if hasattr(self, 'logo_frame') and self.logo_frame.winfo_ismapped():
            self.logo_frame.pack_forget()
        
        # Hide empty state if it exists and is visible
        if hasattr(self, 'empty_state_frame') and self.empty_state_frame.winfo_ismapped():
            self.empty_state_frame.pack_forget()
        
        # Ensure tables_container is packed if not already packed
        if not self.tables_container.winfo_ismapped():
            self.tables_container.pack(fill="both", expand=True, pady=(0, 5))
        
        # Ensure graph frame is packed if not already packed
        if hasattr(self, 'graph_frame') and not self.graph_frame.winfo_ismapped():
            self.graph_frame.pack(fill="both", expand=True)
        
        self.data_visible = True

    def create_data_frames(self) -> None:
        """Create all data frames only once but don't display them initially."""
        
        # Check if tables_container has been created to avoid duplication
        if not hasattr(self, 'tables_container'):
            # Create a container frame for data and chrono tables
            self.tables_container = ttk.Frame(self.right_panel)
            
            # Create Customer Data frame and add Treeview directly
            self.data_frame = ttk.LabelFrame(self.tables_container, text="Customer Data", padding="10")
            self.create_data_frame(self.data_frame)
            self.data_frame.pack(fill="both", expand=True, side="top", pady=(0, 5))
            
            # Create Chronological Order frame and add Treeview directly
            self.chrono_frame = ttk.LabelFrame(self.tables_container, text="Chronological Order of Events", padding="10")
            self.create_chronological_table(self.chrono_frame)
            self.chrono_frame.pack(fill="both", expand=True, side="bottom", pady=5)
        
        # Check if graph_frame has been created to avoid duplication
        if not hasattr(self, 'graph_frame'):
            # Create graph frame separately
            self.graph_frame = ttk.LabelFrame(self.right_panel, text="System State Graph", padding="10")
            self.create_graph_frame(self.graph_frame)

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
        form_frame = ttk.Frame(parent, padding="10", style="Custom.TFrame")
        form_frame.pack(fill="both", expand=True)

        fields = [
            ("Service Code:", "service_code_entry"),
            ("Service Title:", "service_title_entry"),
            ("Duration (min):", "service_duration_entry")
        ]

        for label_text, entry_name in fields:
            container = ttk.Frame(form_frame, style="Custom.TFrame")
            container.pack(fill="x", pady=2)
            
            ttk.Label(
                container,
                text=label_text,
                style="Custom.TLabel"
            ).pack(side="left")
            
            entry = ttk.Entry(
                container,
                style="Custom.TEntry"
            )
            entry.pack(side="right", fill="x", expand=True, padx=(5, 0))
            setattr(self, entry_name, entry)

        add_btn = ttk.Button(
            form_frame,
            text="Add Service",
            command=self.add_service,
            width=20,
            style="ControlFrame.TButton"
        )
        add_btn.pack(pady=5)
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
                self.update_graph()

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
        """Generate random customer data without probability columns."""
        if not self.services:
            messagebox.showerror("Error", "No services available! Please add services first.")
            return

        try:
            self.show_probability_columns = False  # Ensure no probability columns for normal simulation
            num_customers = random.randint(5, 10)
            arrival_time = 0
            new_data = []

            for customer_id in range(1, num_customers + 1):
                interval = random.randint(1, 3)
                arrival_time += interval

                service_code = random.choice(list(self.services.keys()))
                service_info = self.services[service_code]
                service_duration = service_info['duration']
                departure_time = arrival_time + service_duration

                # Add arrival and departure events
                new_data.append({
                    'Customer ID': customer_id,
                    'Event Type': 'Arrival',
                    'Clock Time': arrival_time,
                    'Service Code': service_code,
                    'Service Title': service_info['title'],
                    'Service Duration': service_duration,
                    'End Time': departure_time
                })
                new_data.append({
                    'Customer ID': customer_id,
                    'Event Type': 'Departure',
                    'Clock Time': departure_time,
                    'Service Code': service_code,
                    'Service Title': service_info['title'],
                    'Service Duration': service_duration,
                    'End Time': departure_time
                })

            # Update the DataFrame
            self.current_data = pd.DataFrame(new_data)
            
            # Hide logo screen if visible
            if hasattr(self, 'logo_frame') and self.logo_frame.winfo_ismapped():
                self.logo_frame.pack_forget()
                
            # Show data frames
            self.show_data_frames()
            
            # Update displays
            self.update_displays()
            messagebox.showinfo("Simulation Complete", "Regular simulation completed successfully!")

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

    def update_displays(self) -> None:
        """Update all displays with current data, optionally showing probability columns."""
        self.update_tree()
        self.update_chronological_table()
        self.update_graph()

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

    def update_graph(self) -> None:
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