from abc import ABC, abstractmethod
from io import BytesIO

class IPlotService(ABC):
    @abstractmethod
    def _initialize_plot(self, title):
        pass

    @abstractmethod
    def _generate_empty_plot(self, title):
        pass

    @abstractmethod
    def generate_arrival_and_service_times_plot(self, current_data) -> BytesIO:
        pass

    @abstractmethod
    def generate_customers_in_system_plot(self, current_data) -> BytesIO:
        pass

    @abstractmethod
    def _save_plot_to_output(self, fig) -> BytesIO:
        pass

    def _plot_system_state_data(self, data, ax):
        pass

    def _add_graph_annotations(self, data, ax):
        pass

    def _plot_arrival(self, row, legend_labels):
        pass

    def _plot_waiting(self, row, legend_labels):
        pass

    def _plot_service_duration(self, row, legend_labels):
        pass

    def _plot_departure(self, row, ax):
        pass

    def _configure_plot(self, ax, data):
        pass

    def _configure_graph(self, ax):
        pass