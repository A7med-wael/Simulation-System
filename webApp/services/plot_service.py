from io import BytesIO
import matplotlib.pyplot as plt
from .interfaces.i_plot_service import IPlotService

class PlotService(IPlotService):
    def generate_plot(self, current_data):
        fig, ax = plt.subplots(figsize=(12, 6))

        # Check if there is data to plot
        if not current_data.empty:
            try:
                # Sort data by 'Clock Time' for accurate plotting
                sorted_data = current_data.sort_values('Clock Time')

                # Calculate the cumulative number of customers in the system
                sorted_data['Count Change'] = sorted_data['Event Type'].map({'Arrival': 1, 'Departure': -1})
                sorted_data['Customers in System'] = sorted_data['Count Change'].cumsum()

                # Plot a step graph
                ax.step(sorted_data['Clock Time'], sorted_data['Customers in System'], where='post', color='blue',
                        label='Customers in System')

                # Add annotations for each event
                prev_y = 0
                y_offset = 0
                for _, row in sorted_data.iterrows():
                    current_y = row['Customers in System']

                    # Adjust y_offset to avoid overlapping text
                    if abs(current_y - prev_y) < 0.1:
                        y_offset = (y_offset + 0.2) % 0.6
                    else:
                        y_offset = 0

                    # Annotate each point with customer ID and event type (Arrival/Departure)
                    ax.annotate(
                        f"C{row['Customer ID']}\n{row['Event Type'][0]}",
                        (row['Clock Time'], row['Customers in System'] + y_offset),
                        xytext=(0, 5), textcoords='offset points',
                        ha='center', va='bottom',
                        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                        fontsize=8
                    )
                    prev_y = current_y

                # Configure graph settings
                ax.grid(True, linestyle='--', alpha=0.7)
                ax.set_xlabel('Clock Time')
                ax.set_ylabel('Customers in System')
                ax.set_title('System State Over Time')
                ax.legend()

                # Adjust y-axis limits to prevent clipping of annotations
                y_min, y_max = ax.get_ylim()
                ax.set_ylim(y_min, y_max + 1)

            except Exception as e:
                # Optional: add a flash message or logging here
                print(f"Error updating graph: {e}")

        else:
            # Display a placeholder if there is no data
            ax.text(0.5, 0.5, 'No data to display', horizontalalignment='center', verticalalignment='center')
            ax.set_xticks([])
            ax.set_yticks([])

        # Save the figure to a BytesIO object and send it as an image response
        output = BytesIO()
        plt.savefig(output, format='png')
        plt.close(fig)
        output.seek(0)
        return output
