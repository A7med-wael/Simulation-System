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
        service_end_times = {}  # Dictionary to track when each service is available

        for customer_id in range(1, num_customers + 1):
            # Randomly choose whether to arrive at the same time as the previous customer
            if random.choice([True, False]) or customer_id == 1:
                interval = random.randint(1, 3)
                arrival_time += interval
            else:
                arrival_time = new_data[-1]['Clock Time']  # Same arrival time as the last customer

            # Select a service
            service_code = random.choice(list(services.keys()))
            service_info = services[service_code]
            service_duration = service_info['duration']

            # Determine the departure time, considering available service
            start_service_time = max(arrival_time, service_end_times.get(service_code, arrival_time))
            departure_time = start_service_time + service_duration

            # Update the end time for the service
            service_end_times[service_code] = departure_time

            # Add Arrival and Departure events
            new_data.append({
                'Customer ID': customer_id,
                'Event Type': 'Arrival',
                'Clock Time': arrival_time,
                'Service Code': service_code,
                'Service Title': service_info['title'],
                'Service Duration': service_duration,
                'End Time': departure_time,
                'Waiting Time': start_service_time - arrival_time  # Calculate waiting time
            })
            new_data.append({
                'Customer ID': customer_id,
                'Event Type': 'Departure',
                'Clock Time': departure_time,
                'Service Code': service_code,
                'Service Title': service_info['title'],
                'Service Duration': service_duration,
                'End Time': departure_time,
                'Waiting Time': start_service_time - arrival_time
            })

        return pd.DataFrame(new_data)
