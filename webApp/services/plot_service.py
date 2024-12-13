from io import BytesIO
import matplotlib.pyplot as plt
from .interfaces.i_plot_service import IPlotService

class PlotService(IPlotService):
    def __init__(self):
        pass  # No shared instance data to avoid interference between plots

    def generate_arrival_and_service_times_plot(self, data):
        if data.empty:
            return self._generate_empty_plot("Client Arrival and Service End Times")

        fig, ax = self._initialize_plot("Client Arrival and Service End Times")
        self._plot_arrival_and_service_data(data, ax)
        self._configure_plot(ax, data)
        return self._save_plot_to_output(fig)

    def generate_customers_in_system_plot(self, data):
        if data.empty:
            return self._generate_empty_plot("System State Over Time")

        fig, ax = self._initialize_plot("System State Over Time")
        data_sorted = self._plot_system_state_data(data, ax)
        self._add_graph_annotations(data_sorted, ax)
        self._configure_graph(ax)
        return self._save_plot_to_output(fig)

    def _initialize_plot(self, title):
        plt.style.use('seaborn-v0_8-paper')
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_title(title, fontsize=14)
        return fig, ax

    def _generate_empty_plot(self, title):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'No data to display', horizontalalignment='center', verticalalignment='center', fontsize=14,
                color='gray')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title, fontsize=14)
        return self._save_plot_to_output(fig)

    def _plot_arrival_and_service_data(self, data, ax):
        max_customer_id = data['Customer ID'].max()
        max_end_time = data['End Time'].max()

        for _, row in data.iterrows():
            if row['Event Type'] == 'Arrival':
                self._plot_arrival(row, ax)
                if row['Waiting Time'] > 0:
                    self._plot_waiting(row, ax)
                self._plot_service_duration(row, ax)
            elif row['Event Type'] == 'Departure':
                self._plot_departure(row, ax)

        ax.set_xlim(0, max_end_time + 1)
        ax.set_ylim(0.5, max_customer_id + 1)

    def _plot_system_state_data(self, data, ax):
        """Plot system state data as a step plot and return updated DataFrame."""
        data_sorted = data.sort_values('Clock Time')
        data_sorted['Count Change'] = data_sorted['Event Type'].map({'Arrival': 1, 'Departure': -1})
        data_sorted['Customers in System'] = data_sorted['Count Change'].cumsum()

        ax.step(data_sorted['Clock Time'], data_sorted['Customers in System'],
                where='post', color='blue', linewidth=2, label='Customers in System')

        return data_sorted

    def _add_graph_annotations(self, data, ax):
        """Add annotations to the step plot to indicate events."""
        data_sorted = data.sort_values('Clock Time')
        prev_y = 0
        y_offset = 0

        for _, row in data_sorted.iterrows():
            current_y = row['Customers in System']

            # Adjust y_offset to prevent overlapping annotations
            if abs(current_y - prev_y) < 0.1:
                y_offset = (y_offset + 0.2) % 0.6
            else:
                y_offset = 0

            # Annotate event with Customer ID and Event Type
            ax.annotate(
                f"C{row['Customer ID']}\n{row['Event Type'][0]}",
                (row['Clock Time'], current_y + y_offset),
                xytext=(0, 5), textcoords='offset points',
                ha='center', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                fontsize=8
            )
            prev_y = current_y

    def _configure_graph(self, ax):
        """Configure plot with additional styling and axis limits."""
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_xlabel('Clock Time', fontsize=12)
        ax.set_ylabel('Customers in System', fontsize=12)
        ax.set_title('System State Over Time', fontsize=14)
        ax.legend(loc='upper left', fontsize=10)

        # Adjust y-axis limits to add padding for annotations
        y_min, y_max = ax.get_ylim()
        ax.set_ylim(y_min, y_max + 1)

    def _plot_arrival(self, row, ax):
        ax.plot(row['Clock Time'], row['Customer ID'], 'o', color='blue',
                label='Arrival Time' if 'Arrival Time' not in ax.get_legend_handles_labels()[1] else None, markersize=6)

    def _plot_waiting(self, row, ax):
        waiting_start = row['Clock Time']
        waiting_end = row['Clock Time'] + row['Waiting Time']
        ax.plot([waiting_start, waiting_end], [row['Customer ID'], row['Customer ID']], color='orange', linestyle='--',
                linewidth=2, label='Waiting Time' if 'Waiting Time' not in ax.get_legend_handles_labels()[1] else None)

        ax.annotate(
            f'Wait: {row["Waiting Time"]}',
            (waiting_start + row['Waiting Time'] / 2, row['Customer ID'] + 0.15),
            textcoords="offset points", xytext=(0, 10), ha='center', fontsize=10, color='black'
        )

    def _plot_service_duration(self, row, ax):
        service_start = row['Clock Time'] + row['Waiting Time'] if row['Waiting Time'] > 0 else row['Clock Time']
        ax.plot([service_start, row['End Time']], [row['Customer ID'], row['Customer ID']], color='green', linewidth=2,
                label='Service Duration' if 'Service Duration' not in ax.get_legend_handles_labels()[1] else None)

    def _plot_departure(self, row, ax):
        ax.plot(row['End Time'], row['Customer ID'], 'o', color='red',
                label='End Time' if 'End Time' not in ax.get_legend_handles_labels()[1] else None)

    def _configure_plot(self, ax, data):
        max_end_time = data['End Time'].max()
        max_customer_id = data['Customer ID'].max()
        ax.set_xticks(range(int(max_end_time) + 2))
        ax.set_yticks(range(1, int(max_customer_id) + 1))
        ax.set_xlabel("Time", fontsize=12)
        ax.set_ylabel("Client Number", fontsize=12)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.7)

    def _save_plot_to_output(self, fig):
        output = BytesIO()
        fig.savefig(output, format='png')
        plt.close(fig)
        output.seek(0)
        return output

    def generate_parallel_servers_plot(self, data):
        """Generate a plot showing parallel server timelines and customer events."""
        if data.empty:
            return self._generate_empty_plot("Parallel Servers Simulation Timeline")

        fig, ax = self._initialize_plot("Parallel Servers Simulation Timeline")
        self._plot_server_timelines(ax, data)
        self._plot_customer_events(ax, data)
        self._configure_multi_server_plot(ax, data)
        return self._save_plot_to_output(fig)

    def _plot_server_timelines(self, ax, data):
        """Plot horizontal timelines for each server on the graph."""
        ax.get_figure().set_facecolor('white')

        server_positions = {'Able': 1, 'Baker': 2}
        for server, position in server_positions.items():
            ax.hlines(
                position, 0, data['End Time'].max(),
                colors='gray', linestyles='--', alpha=0.3,
                label=f'{server} Timeline'
            )

    def _plot_customer_events(self, ax, data):
        """Plot customer arrival, waiting, and service events."""
        server_positions = {'Able': 1, 'Baker': 2}
        colors = {'Able': '#2ecc71', 'Baker': '#3498db'}

        # Track which labels have been added to avoid duplicates
        labels_added = {'Arrival': False, 'Wait Time': False, 'Able Service': False, 'Baker Service': False}

        for _, row in data.iterrows():
            server_pos = server_positions[row['Server']]
            service_start = row['Clock Time'] + row['Wait Time']

            # Arrival point
            ax.scatter(row['Clock Time'], 0, color='#e74c3c', marker='o',
                       label='Arrival' if not labels_added['Arrival'] else "")
            labels_added['Arrival'] = True

            # Waiting timeline (if any)
            if row['Wait Time'] > 0:
                ax.vlines(row['Clock Time'], 0, server_pos,
                          colors='#f1c40f', linestyles=':',
                          label='Wait Time' if not labels_added['Wait Time'] else "")
                labels_added['Wait Time'] = True

            # Service duration with separate labels for Able and Baker
            service_label = f'{row["Server"]} Service'
            ax.hlines(server_pos, service_start, row['End Time'],
                      colors=colors[row['Server']], linewidth=6, alpha=0.7,
                      label=service_label if not labels_added[service_label] else "")
            labels_added[service_label] = True

           # ** Add points at the start and end of the service duration **
            ax.scatter(service_start, server_pos, color=colors[row['Server']], marker='o', 
                label=f'Start {row["Server"]}' if f'Start {row["Server"]}' not in labels_added else "")
            ax.scatter(row['End Time'], server_pos, color=colors[row['Server']], marker='o',
                   label=f'End {row["Server"]}' if f'End {row["Server"]}' not in labels_added else "")

            # Customer ID label
            ax.text(row['Clock Time'], -0.2, f'C{row["Customer ID"]}',
                    fontsize=8, rotation=45, ha='right', va='top')

    def _configure_multi_server_plot(self, ax, data):
        """Customize the plot with labels, legends, and axis settings."""
        ax.set_ylim(-0.5, 2.5)
        ax.set_xlim(-2, data['End Time'].max() + 2)
        ax.set_yticks([0, 1, 2])
        ax.set_yticklabels(['Arrivals', 'Server Able', 'Server Baker'])

        ax.set_xlabel('Time (minutes)', fontsize=12)
        ax.set_title('Parallel Servers Simulation Timeline', fontsize=14)
        ax.grid(True, alpha=0.2)

        # Add legend, ensuring unique entries
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1, 1))