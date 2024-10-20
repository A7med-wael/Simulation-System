import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import random
from typing import Dict, Any

class QueuingSystemGUI:
    def __init__(self, root: tk.Tk) -> None:
        """Initialize the Queuing System GUI."""
        self.root = root
        self.root.title("Queuing System Simulation")
        self.root.geometry("1200x800")
        
        # Configure style
        self.setup_style()
        
        # Initialize data structures
        self.initialize_data()
        
        # Create main container
        self.main_container = ttk.Frame(self.root, style="Custom.TFrame")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Setup GUI components
        self.setup_gui()

    def setup_style(self) -> None:
        """Configure the application style."""
        style = ttk.Style()
        style.configure("TLabelframe", padding=10)
        style.configure("TButton", padding=5)
        style.configure("Custom.TFrame", background="#f0f0f0")

    def initialize_data(self) -> None:
        """Initialize data structures."""
        self.data_file_path = "queuing_data.xlsx"
        self.current_data = pd.DataFrame(columns=[
            'Customer ID', 'Event Type', 'Clock Time', 
            'Service Code', 'Service Title', 'Service Duration', 'End Time'
        ])
        self.services: Dict[str, Dict[str, Any]] = {}

    def setup_gui(self) -> None:
        """Setup the main GUI components."""
        # Create left panel
        left_panel = ttk.Frame(self.main_container)
        left_panel.pack(side="left", fill="y", padx=(0, 5))
        
        # Create right panel
        right_panel = ttk.Frame(self.main_container)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Setup GUI components
        self.create_control_frame(left_panel)
        self.create_service_form(left_panel)
        self.create_data_frame(right_panel)
        self.create_chronological_table(right_panel)
        self.create_graph_frame(right_panel)

    def create_control_frame(self, parent: ttk.Frame) -> None:
        """Create the control buttons frame."""
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.pack(fill="x", pady=(0, 5))

        btn_configs = [
            ("Upload Data", self.upload_file, "Upload service data from file"),
            ("Simulate", self.generate_customers, "Generate new customer data"),
            ("Save All", self.save_all_data, "Save current simulation data"),
            ("Clear All", self.clear_all_data, "Clear all current data")
        ]

        for text, command, tooltip in btn_configs:
            btn = ttk.Button(control_frame, text=text, command=command, width=20)
            btn.pack(pady=2)
            self.create_tooltip(btn, tooltip)

    def create_service_form(self, parent: ttk.Frame) -> None:
        """Create the service input form."""
        form_frame = ttk.LabelFrame(parent, text="Add New Service", padding="10")
        form_frame.pack(fill="x", pady=5)

        fields = [
            ("Service Code:", "service_code_entry"),
            ("Service Title:", "service_title_entry"),
            ("Duration (min):", "service_duration_entry")
        ]

        for label_text, entry_name in fields:
            container = ttk.Frame(form_frame)
            container.pack(fill="x", pady=2)
            
            ttk.Label(container, text=label_text).pack(side="left")
            entry = ttk.Entry(container)
            entry.pack(side="right", fill="x", expand=True, padx=(5, 0))
            setattr(self, entry_name, entry)

        add_btn = ttk.Button(form_frame, text="Add Service", command=self.add_service, width=20)
        add_btn.pack(pady=5)

    def create_data_frame(self, parent: ttk.Frame) -> None:
        """Create the main data display frame."""
        data_frame = ttk.LabelFrame(parent, text="Customer Data", padding="10")
        data_frame.pack(fill="both", expand=True, pady=(0, 5))

        columns = ("Customer ID", "Event Type", "Clock Time", "Service Code", 
                  "Service Title", "Service Duration", "End Time")
        
        self.tree = ttk.Treeview(data_frame, columns=columns, show="headings")

        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Add scrollbars
        self.add_scrollbars(data_frame, self.tree)

    def create_chronological_table(self, parent: ttk.Frame) -> None:
        """Create the chronological events table."""
        chrono_frame = ttk.LabelFrame(parent, text="Chronological Order of Events", padding="10")
        chrono_frame.pack(fill="both", expand=True, pady=5)

        columns = ("Time", "Event Type", "Customer ID", "Service")
        self.chrono_tree = ttk.Treeview(chrono_frame, columns=columns, show="headings", height=5)

        # Configure columns
        column_widths = {"Time": 100, "Event Type": 100, "Customer ID": 100, "Service": 200}
        for col, width in column_widths.items():
            self.chrono_tree.heading(col, text=col)
            self.chrono_tree.column(col, width=width)

        # Add scrollbars
        self.add_scrollbars(chrono_frame, self.chrono_tree)

    def create_graph_frame(self, parent: ttk.Frame) -> None:
        """Create the graph display frame."""
        self.graph_frame = ttk.LabelFrame(parent, text="System State Graph", padding="10")
        self.graph_frame.pack(fill="both", expand=True)
        
        self.figure, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.update_graph()

    def add_scrollbars(self, parent: ttk.Frame, widget: ttk.Treeview) -> None:
        """Add scrollbars to a widget."""
        y_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=widget.yview)
        x_scrollbar = ttk.Scrollbar(parent, orient="horizontal", command=widget.xview)
        widget.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        x_scrollbar.pack(side="bottom", fill="x")
        y_scrollbar.pack(side="right", fill="y")
        widget.pack(side="left", fill="both", expand=True)

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
        """Generate random customer data."""
        if not self.services:
            messagebox.showerror("Error", "No services available! Please add services first.")
            return

        try:
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

            self.current_data = pd.DataFrame(new_data)
            self.update_displays()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate customers: {str(e)}")

    def update_displays(self) -> None:
        """Update all displays with current data."""
        self.update_tree()
        self.update_chronological_table()
        self.update_graph()

    def update_tree(self) -> None:
        """Update the main data tree view."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.current_data.empty:
            sorted_data = self.current_data.sort_values('Clock Time')
            for _, row in sorted_data.iterrows():
                self.tree.insert("", "end", values=tuple(row))

    def update_chronological_table(self) -> None:
        """Update the chronological events table."""
        for item in self.chrono_tree.get_children():
            self.chrono_tree.delete(item)

        if not self.current_data.empty:
            sorted_data = self.current_data.sort_values('Clock Time')
            for _, row in sorted_data.iterrows():
                self.chrono_tree.insert("", "end", values=(
                    f"Time {row['Clock Time']}",
                    row['Event Type'],
                    f"Customer {row['Customer ID']}",
                    row['Service Title']
                ))

    def update_graph(self) -> None:
        """Update the system state graph."""
        self.ax.clear()
        
        if not self.current_data.empty:
            try:
                sorted_data = self.current_data.sort_values('Clock Time')
                sorted_data['Count Change'] = sorted_data['Event Type'].map({'Arrival': 1, 'Departure': -1})
                sorted_data['Customers in System'] = sorted_data['Count Change'].cumsum()

                # Plot step graph
                self.ax.step(sorted_data['Clock Time'], sorted_data['Customers in System'], 
                           where='post', color='blue', label='Customers in System')
                
                # Add annotations
                self._add_graph_annotations(sorted_data)

                # Configure graph
                self._configure_graph()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update graph: {str(e)}")
        else:
            self._show_empty_graph()

        self.canvas.draw()

    def _add_graph_annotations(self, sorted_data: pd.DataFrame) -> None:
        """Add annotations to the graph."""
        prev_y = 0
        y_offset = 0
        for _, row in sorted_data.iterrows():
            current_y = row['Customers in System']
            
            # Adjust y_offset to prevent overlap
            if abs(current_y - prev_y) < 0.1:
                y_offset = (y_offset + 0.2) % 0.6
            else:
                y_offset = 0
            
            # Add annotation
            self.ax.annotate(
                f"C{row['Customer ID']}\n{row['Event Type'][0]}",
                (row['Clock Time'], row['Customers in System'] + y_offset),
                xytext=(0, 5), textcoords='offset points',
                ha='center', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                fontsize=8
            )
            prev_y = current_y

    def _configure_graph(self) -> None:
        """Configure graph settings."""
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.set_xlabel('Clock Time')
        self.ax.set_ylabel('Customers in System')
        self.ax.set_title('System State Over Time')
        self.ax.legend()
        
        # Adjust y-axis limits
        y_min, y_max = self.ax.get_ylim()
        self.ax.set_ylim(y_min, y_max + 1)

    def _show_empty_graph(self) -> None:
        """Show empty graph placeholder."""
        self.ax.text(0.5, 0.5, 'No data to display', 
                    horizontalalignment='center', verticalalignment='center')
        self.ax.set_xticks([])
        self.ax.set_yticks([])

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

    def clear_all_data(self) -> None:
        """Clear all current data and reset displays."""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all data?"):
            try:
                self.current_data = pd.DataFrame(columns=[
                    'Customer ID', 'Event Type', 'Clock Time', 'Service Code', 
                    'Service Title', 'Service Duration', 'End Time'
                ])
                self.update_displays()
                messagebox.showinfo("Success", "All data cleared successfully!")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear data: {str(e)}")

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