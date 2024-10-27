from abc import ABC, abstractmethod

class ISimulationService(ABC):
    @abstractmethod
    def simulate_customers(self, services: dict) -> dict:
        pass
