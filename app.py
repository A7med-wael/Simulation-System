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
        self.root.title("Enhanced Queuing System Simulation")
        self.root.geometry("1000x800")
        
        # Initialize data storage
        self.data_file_path = "queuing_data.xlsx"
        self.current_data = pd.DataFrame(columns=['Customer ID', 'Event Type', 'Clock Time', 'Service Code', 'Service Title', 'Service Duration'])

        # Define service dictionary (service code -> title, duration)
        self.services = {
            'A': {'title': 'Consultation', 'duration': 5},
            'B': {'title': 'Follow-up', 'duration': 3},
            'C': {'title': 'Diagnostic', 'duration': 7}
        }

        self.setup_gui()

    def setup_gui(self):
        self.create_control_frame()
        self.create_data_frame()
        self.create_graph_frame()

    def create_control_frame(self):
        control_frame = ttk.LabelFrame(self.root, text="Controls", padding="10")
        control_frame.pack(fill="x", padx=10, pady=5)

        file_frame = ttk.Frame(control_frame)
        file_frame.pack(fill="x", pady=5)
        ttk.Button(file_frame, text="Upload Data", command=self.upload_file).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Simulate the system", command=self.generate_customers).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Save All Data", command=self.save_all_data).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Clear All", command=self.clear_all_data).pack(side="left", padx=5)

    def create_data_frame(self):
        data_frame = ttk.LabelFrame(self.root, text="Customer Data", padding="10")
        data_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(data_frame, columns=("Customer ID", "Event Type", "Clock Time", "Service Code", 
                                                      "Service Title", "Service Duration"), show="headings")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_graph_frame(self):
        self.graph_frame = ttk.LabelFrame(self.root, text="System State Graph", padding="10")
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def generate_customers(self):
        self.clear_all_data()

        num_customers = 7
        arrival_time = 0  # Start at time 0

        for customer_id in range(1, num_customers + 1):
            # Generate random interval and update arrival time
            interval = random.randint(0, 3)
            arrival_time += interval

            # Assign a random service
            service_code = random.choice(list(self.services.keys()))
            service_title = self.services[service_code]['title']
            service_duration = self.services[service_code]['duration']

            # Calculate departure time
            departure_time = arrival_time + service_duration

            # Add arrival event
            self.add_event(customer_id, 'Arrival', arrival_time, service_code, service_title, service_duration)

            # Add departure event
            self.add_event(customer_id, 'Departure', departure_time, service_code, service_title, service_duration)

        self.update_tree()
        self.update_graph()

    def add_event(self, customer_id, event_type, clock_time, service_code, service_title, service_duration):
        event_data = {
            'Customer ID': customer_id,
            'Event Type': event_type,
            'Clock Time': clock_time,
            'Service Code': service_code,
            'Service Title': service_title,
            'Service Duration': service_duration
        }
        self.current_data = pd.concat([self.current_data, pd.DataFrame([event_data])], ignore_index=True)

    def update_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        sorted_data = self.current_data.sort_values('Clock Time')
        for _, row in sorted_data.iterrows():
            self.tree.insert("", "end", values=tuple(row))

    def update_graph(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        if len(self.current_data) > 0:
            sorted_data = self.current_data.sort_values('Clock Time')
            sorted_data['Count Change'] = sorted_data['Event Type'].map({'Arrival': 1, 'Departure': -1})
            sorted_data['Customers in System'] = sorted_data['Count Change'].cumsum()

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.step(sorted_data['Clock Time'], sorted_data['Customers in System'], where='post', label='Customers in System', color='blue')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_xlabel('Clock Time')
            ax.set_ylabel('Number of Customers')
            ax.set_title('System State Over Time')
            ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if file_path:
            try:
                # Read the file
                if file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                else:
                    df = pd.read_csv(file_path)
                
                # Check and standardize column names
                required_columns = {'Customer ID', 'Event Type', 'Clock Time', 'Service Time'}
                
                # Convert column names to title case and remove extra spaces
                df.columns = [col.strip().title() for col in df.columns]
                
                # Check if we have all required columns
                if not required_columns.issubset(set(df.columns)):
                    # Try to map common alternative names
                    column_mapping = {
                        'Customer': 'Customer ID',
                        'Customer Id': 'Customer ID',
                        'CustomerId': 'Customer ID',
                        'ID': 'Customer ID',
                        'Event': 'Event Type',
                        'EventType': 'Event Type',
                        'Time': 'Clock Time',
                        'ClockTime': 'Clock Time',
                        'Service': 'Service Time',
                        'ServiceTime': 'Service Time'
                    }
                    
                    # Try to rename columns if possible
                    df = df.rename(columns=column_mapping)
                    
                    # Check again after renaming
                    if not required_columns.issubset(set(df.columns)):
                        missing_cols = required_columns - set(df.columns)
                        messagebox.showerror("Error", 
                            f"The uploaded file is missing required columns: {', '.join(missing_cols)}\n\n"
                            f"Required columns are: {', '.join(required_columns)}\n\n"
                            f"Found columns: {', '.join(df.columns)}")
                        return
                
                # Ensure numeric types for time columns
                try:
                    df['Clock Time'] = pd.to_numeric(df['Clock Time'])
                    df['Service Time'] = pd.to_numeric(df['Service Time'])
                except Exception:
                    messagebox.showerror("Error", 
                        "Time values must be numeric. Please check your data.")
                    return
                
                # Update current data
                self.current_data = df
                
                # Update display
                self.update_tree()
                self.update_graph()
                messagebox.showinfo("Success", "File loaded successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", 
                    f"Error loading file: {str(e)}\n\nPlease ensure your file has the correct format.")
    def save_all_data(self):
        if len(self.current_data) > 0:
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
            if file_path:
                try:
                    self.current_data.to_excel(file_path, index=False) if file_path.endswith('.xlsx') else self.current_data.to_csv(file_path, index=False)
                    messagebox.showinfo("Success", "Data saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def clear_all_data(self):
        self.current_data = pd.DataFrame(columns=['Customer ID', 'Event Type', 'Clock Time', 'Service Code', 'Service Title', 'Service Duration'])
        self.update_tree()
        self.update_graph()

if __name__ == "__main__":
    root = tk.Tk()
    app = QueuingSystemGUI(root)
    root.mainloop()
