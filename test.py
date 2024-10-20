import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import random

class QueuingSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Queuing System Simulation")
        self.root.geometry("1200x800")
        
        # Apply a theme for better appearance
        style = ttk.Style()
        style.configure("TLabelframe", padding=10)
        style.configure("TButton", padding=5)
        style.configure("Custom.TFrame", background="#f0f0f0")

        # Initialize data storage
        self.data_file_path = "queuing_data.xlsx"
        self.current_data = pd.DataFrame(columns=[
            'Customer ID', 'Event Type', 'Clock Time', 
            'Service Code', 'Service Title', 'Service Duration', 'End Time'
        ])

        # Initialize services
        self.services = {}
        
        # Create main container
        self.main_container = ttk.Frame(self.root, style="Custom.TFrame")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.setup_gui()

    def setup_gui(self):
        # Left panel for controls and service form
        left_panel = ttk.Frame(self.main_container)
        left_panel.pack(side="left", fill="y", padx=(0, 5))
        
        # Right panel for data and graph
        right_panel = ttk.Frame(self.main_container)
        right_panel.pack(side="right", fill="both", expand=True)
        
        self.create_control_frame(left_panel)
        self.create_service_form(left_panel)
        self.create_data_frame(right_panel)
        self.create_graph_frame(right_panel)

    def create_control_frame(self, parent):
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

    def create_service_form(self, parent):
        form_frame = ttk.LabelFrame(parent, text="Add New Service", padding="10")
        form_frame.pack(fill="x", pady=5)

        # Service form fields
        fields = [
            ("Service Code:", "service_code_entry"),
            ("Service Title:", "service_title_entry"),
            ("Duration (min):", "service_duration_entry")
        ]

        for i, (label_text, entry_name) in enumerate(fields):
            container = ttk.Frame(form_frame)
            container.pack(fill="x", pady=2)
            
            ttk.Label(container, text=label_text).pack(side="left")
            entry = ttk.Entry(container)
            entry.pack(side="right", fill="x", expand=True, padx=(5, 0))
            setattr(self, entry_name, entry)

        ttk.Button(form_frame, text="Add Service", command=self.add_service, width=20).pack(pady=5)

    def create_data_frame(self, parent):
        data_frame = ttk.LabelFrame(parent, text="Customer Data", padding="10")
        data_frame.pack(fill="both", expand=True, pady=(0, 5))

        # Create Treeview with scrollbar
        self.tree = ttk.Treeview(data_frame, columns=(
            "Customer ID", "Event Type", "Clock Time", "Service Code", 
            "Service Title", "Service Duration", "End Time"
        ), show="headings")

        # Configure columns
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(data_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Pack elements
        x_scrollbar.pack(side="bottom", fill="x")
        y_scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

    def create_graph_frame(self, parent):
        self.graph_frame = ttk.LabelFrame(parent, text="System State Graph", padding="10")
        self.graph_frame.pack(fill="both", expand=True)
        
        # Create placeholder for graph
        self.figure, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Initialize empty graph
        self.update_graph()

    def create_tooltip(self, widget, text):
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
                del widget.tooltip

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def add_service(self):
        code = self.service_code_entry.get()
        title = self.service_title_entry.get()
        try:
            duration = int(self.service_duration_entry.get())
            if code and title:
                self.services[code] = {'title': title, 'duration': duration}
                messagebox.showinfo("Success", f"Service {title} added successfully!")
                # Clear entries
                for entry in [self.service_code_entry, self.service_title_entry, self.service_duration_entry]:
                    entry.delete(0, 'end')
            else:
                messagebox.showerror("Error", "Please fill all fields.")
        except ValueError:
            messagebox.showerror("Error", "Duration must be a number.")

    def generate_customers(self):
        if not self.services:
            messagebox.showerror("Error", "No services available! Please add services first.")
            return

        num_customers = random.randint(5, 10)  # Random number of customers between 5 and 10
        arrival_time = 0

        new_data = []
        for customer_id in range(1, num_customers + 1):
            interval = random.randint(1, 3)
            arrival_time += interval

            service_code = random.choice(list(self.services.keys()))
            service_info = self.services[service_code]
            service_duration = service_info['duration']
            departure_time = arrival_time + service_duration

            # Add arrival event
            new_data.append({
                'Customer ID': customer_id,
                'Event Type': 'Arrival',
                'Clock Time': arrival_time,
                'Service Code': service_code,
                'Service Title': service_info['title'],
                'Service Duration': service_duration,
                'End Time': departure_time
            })

            # Add departure event
            new_data.append({
                'Customer ID': customer_id,
                'Event Type': 'Departure',
                'Clock Time': departure_time,
                'Service Code': service_code,
                'Service Title': service_info['title'],
                'Service Duration': service_duration,
                'End Time': departure_time
            })

        self.current_data = pd.DataFrame(new_data)
        self.update_tree()
        self.update_graph()

    def update_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        sorted_data = self.current_data.sort_values('Clock Time')
        for _, row in sorted_data.iterrows():
            self.tree.insert("", "end", values=tuple(row))

    def update_graph(self):
        self.ax.clear()
        
        if not self.current_data.empty:
            sorted_data = self.current_data.sort_values('Clock Time')
            sorted_data['Count Change'] = sorted_data['Event Type'].map({'Arrival': 1, 'Departure': -1})
            sorted_data['Customers in System'] = sorted_data['Count Change'].cumsum()

            self.ax.step(sorted_data['Clock Time'], sorted_data['Customers in System'], 
                        where='post', color='blue', label='Customers in System')
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.ax.set_xlabel('Clock Time')
            self.ax.set_ylabel('Customers in System')
            self.ax.set_title('System State Over Time')
            self.ax.legend()
        else:
            self.ax.text(0.5, 0.5, 'No data to display', 
                        horizontalalignment='center', verticalalignment='center')
            self.ax.set_xticks([])
            self.ax.set_yticks([])
        
        self.canvas.draw()

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        
        if file_path:
            try:
                df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
                required_columns = ['Service Code', 'Service Title', 'Service Duration (minutes)']
                
                if not all(col in df.columns for col in required_columns):
                    messagebox.showerror("Error", 
                        "Invalid file format! Required columns: 'Service Code', 'Service Title', and 'Service Duration (minutes)'")
                    return
                
                self.services.clear()
                for _, row in df.iterrows():
                    self.services[row['Service Code']] = {
                        'title': row['Service Title'],
                        'duration': int(row['Service Duration (minutes)'])
                    }
                
                messagebox.showinfo("Success", f"Successfully loaded {len(self.services)} services!")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def save_all_data(self):
        if self.current_data.empty:
            messagebox.showwarning("Warning", "No data to save!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
            
        if file_path:
            try:
                self.current_data.to_excel(file_path, index=False)
                messagebox.showinfo("Success", "Data saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save data: {str(e)}")

    def clear_all_data(self):
        self.current_data = pd.DataFrame(columns=[
            'Customer ID', 'Event Type', 'Clock Time', 'Service Code', 
            'Service Title', 'Service Duration', 'End Time'
        ])
        self.update_tree()
        self.update_graph()

if __name__ == "__main__":
    root = tk.Tk()
    app = QueuingSystemGUI(root)
    root.mainloop()