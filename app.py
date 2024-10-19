import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class QueuingSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Queuing System Simulation")
        self.root.geometry("1000x800")
        
        # Initialize data storage
        self.data_file_path = "queuing_data.xlsx"
        self.current_data = pd.DataFrame(columns=['Customer ID', 'Event Type', 'Clock Time', 'Service Time'])
        
        self.setup_gui()

    def setup_gui(self):
        # Create main frames
        self.create_control_frame()
        self.create_data_frame()
        self.create_graph_frame()

    def create_control_frame(self):
        control_frame = ttk.LabelFrame(self.root, text="Controls", padding="10")
        control_frame.pack(fill="x", padx=10, pady=5)

        # File operations
        file_frame = ttk.Frame(control_frame)
        file_frame.pack(fill="x", pady=5)

        ttk.Button(file_frame, text="Upload Data", command=self.upload_file).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Save All Data", command=self.save_all_data).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Clear All", command=self.clear_all_data).pack(side="left", padx=5)

        # Input frame
        input_frame = ttk.Frame(control_frame)
        input_frame.pack(fill="x", pady=10)

        # Customer ID
        ttk.Label(input_frame, text="Customer ID:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_customer_id = ttk.Entry(input_frame)
        self.entry_customer_id.grid(row=0, column=1, padx=5, pady=5)

        # Arrival Time
        ttk.Label(input_frame, text="Arrival Time:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_arrival_time = ttk.Entry(input_frame)
        self.entry_arrival_time.grid(row=0, column=3, padx=5, pady=5)

        # Service Time
        ttk.Label(input_frame, text="Service Time:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_service_time = ttk.Entry(input_frame)
        self.entry_service_time.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(input_frame, text="Add Customer", command=self.add_customer).grid(row=0, column=6, padx=5, pady=5)

    def create_data_frame(self):
        data_frame = ttk.LabelFrame(self.root, text="Customer Data", padding="10")
        data_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create Treeview
        self.tree = ttk.Treeview(data_frame, columns=("Customer ID", "Event Type", "Clock Time", "Service Time"), 
                                show="headings")
        
        # Set column headings
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack elements
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_graph_frame(self):
        self.graph_frame = ttk.LabelFrame(self.root, text="System State Graph", padding="10")
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def add_customer(self):
        try:
            customer_id = self.entry_customer_id.get()
            arrival_time = int(self.entry_arrival_time.get())
            service_time = int(self.entry_service_time.get())
            departure_time = arrival_time + service_time

            # Add arrival event
            arrival_data = {
                'Customer ID': customer_id,
                'Event Type': 'Arrival',
                'Clock Time': arrival_time,
                'Service Time': service_time
            }
            
            # Add departure event
            departure_data = {
                'Customer ID': customer_id,
                'Event Type': 'Departure',
                'Clock Time': departure_time,
                'Service Time': service_time
            }

            # Add to DataFrame
            self.current_data = pd.concat([self.current_data, 
                                         pd.DataFrame([arrival_data, departure_data])], 
                                         ignore_index=True)

            # Update tree and graph
            self.update_tree()
            self.update_graph()
            self.clear_entries()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for times.")

    def update_tree(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Sort data by clock time
        sorted_data = self.current_data.sort_values('Clock Time')
        
        # Add sorted data to tree
        for _, row in sorted_data.iterrows():
            self.tree.insert("", "end", values=tuple(row))

    def update_graph(self):
        # Clear existing graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        if len(self.current_data) > 0:
            # Sort data by clock time
            sorted_data = self.current_data.sort_values('Clock Time')
            
            # Calculate customer count
            sorted_data['Count Change'] = sorted_data['Event Type'].map({'Arrival': 1, 'Departure': -1})
            sorted_data['Customers in System'] = sorted_data['Count Change'].cumsum()

            # Create figure
            fig, ax = plt.subplots(figsize=(10, 4))
            
            # Plot the step graph
            times = sorted_data['Clock Time'].tolist()
            counts = sorted_data['Customers in System'].tolist()
            
            ax.step(times, counts, where='post', label='Customers in System', color='blue')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_xlabel('Clock Time')
            ax.set_ylabel('Number of Customers')
            ax.set_title('System State Over Time')
            
            # Ensure y-axis shows integer values
            ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

            # Create canvas
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

    def clear_entries(self):
        self.entry_customer_id.delete(0, 'end')
        self.entry_arrival_time.delete(0, 'end')
        self.entry_service_time.delete(0, 'end')

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
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
            )
            if file_path:
                try:
                    if file_path.endswith('.xlsx'):
                        self.current_data.to_excel(file_path, index=False)
                    else:
                        self.current_data.to_csv(file_path, index=False)
                    messagebox.showinfo("Success", "Data saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def clear_all_data(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all data?"):
            self.current_data = pd.DataFrame(columns=['Customer ID', 'Event Type', 'Clock Time', 'Service Time'])
            self.update_tree()
            self.update_graph()

if __name__ == "__main__":
    root = tk.Tk()
    app = QueuingSystemGUI(root)
    root.mainloop()