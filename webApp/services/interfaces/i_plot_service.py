from abc import ABC, abstractmethod
from io import BytesIO

class IPlotService(ABC):
    @abstractmethod
    def generate_plot(self, current_data) -> BytesIO:
        pass
