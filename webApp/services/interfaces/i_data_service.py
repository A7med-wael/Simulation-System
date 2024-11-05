from abc import ABC, abstractmethod
from io import BytesIO


class IDataService(ABC):
    @abstractmethod
    def add_service(self, code: str, title: str, duration: int) -> dict:
        pass

    @abstractmethod
    def upload_services_from_file(self, file) -> dict:
        pass

    @abstractmethod
    def clear_data(self):
        pass

    @abstractmethod
    def download_data(self) -> BytesIO:
        pass

    def validate_numeric_data(self, *values):
        pass
