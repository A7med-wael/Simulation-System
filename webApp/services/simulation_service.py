import random
import pandas as pd
from flask import jsonify

from .interfaces.i_simulation_service import ISimulationService


class SimulationService(ISimulationService):
    def simulate_customers(self, services):
        if not services:
            return jsonify({'success': False, 'error': 'No services available!'})

        num_customers = random.randint(5, 10)
        arrival_time = 0
        new_data = []
        for customer_id in range(1, num_customers + 1):
            interval = random.randint(1, 3)
            arrival_time += interval
            service_code = random.choice(list(services.keys()))
            service_info = services[service_code]
            service_duration = service_info['duration']
            departure_time = arrival_time + service_duration
            for event_type in ['Arrival', 'Departure']:
                event_time = arrival_time if event_type == 'Arrival' else departure_time
                new_data.append({
                    'Customer ID': customer_id,
                    'Event Type': event_type,
                    'Clock Time': event_time,
                    'Service Code': service_code,
                    'Service Title': service_info['title'],
                    'Service Duration': service_duration,
                    'End Time': departure_time
                })
        return pd.DataFrame(new_data)
