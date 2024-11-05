from abc import ABC, abstractmethod

class ISimulationService(ABC):
    @abstractmethod
    def simulate_customers(self, services: dict) -> dict:
        pass

    def extract_probability_data(self, tree):
        pass

    def initialize_servers(self, server_names):
        pass

    def assign_server(self, servers, arrival_time):
        pass



    def create_customer_info(self, customers, arrival_time, assigned_server, service_time, servers):
        pass

    def calculate_metrics(self, df_customers, servers, simulation_period):
        pass
