import random
import pandas as pd
from flask import jsonify
from .interfaces.i_simulation_service import ISimulationService

class SimulationService(ISimulationService):
    def simulate_customers(self, services, probability_simulation=False):
        if not services:
            return jsonify({'success': False, 'error': 'No services available!'})

        arrival_probability = 0.6
        service_completion_probability = 0.8
        num_customers = random.randint(5, 10)
        arrival_time = 0
        new_data = []
        service_end_times = {}
        assigned_customer_ids = []  # List to track assigned customer IDs

        for _ in range(num_customers):
            if random.random() <= arrival_probability:
                customer_id = len(assigned_customer_ids) + 1  # Unique ID based on the count of assigned IDs
                assigned_customer_ids.append(customer_id)  # Add to the list of assigned IDs

                if random.choice([True, False]) or customer_id == 1:
                    interval = random.randint(1, 3)
                    arrival_time += interval
                else:
                    # Ensure new_data is not empty before accessing
                    if new_data:
                        arrival_time = new_data[-1]['Clock Time']
                    else:
                        # If new_data is empty, reset arrival_time to 0 or some default
                        arrival_time = 0

                service_code = random.choice(list(services.keys()))
                service_info = services[service_code]
                service_duration = service_info['duration']
                start_service_time = max(arrival_time, service_end_times.get(service_code, arrival_time))
                departure_time = start_service_time + service_duration

                service_end_times[service_code] = departure_time

                arrival_prob = round(random.random(), 2) if probability_simulation else None
                completion_prob = round(service_completion_probability, 2) if probability_simulation else None

                base_event_data = {
                    'Customer ID': customer_id,
                    'Event Type': 'Arrival',
                    'Clock Time': arrival_time,
                    'Service Code': service_code,
                    'Service Title': service_info['title'],
                    'Service Duration': service_duration,
                    'End Time': departure_time,
                    'Waiting Time': start_service_time - arrival_time
                }

                if probability_simulation:
                    base_event_data['Arrival Probability'] = arrival_prob
                    base_event_data['Completion Probability'] = completion_prob

                new_data.append(base_event_data)

                base_event_data = {
                    'Customer ID': customer_id,
                    'Event Type': 'Departure',
                    'Clock Time': departure_time,
                    'Service Code': service_code,
                    'Service Title': service_info['title'],
                    'Service Duration': service_duration,
                    'End Time': departure_time,
                    'Waiting Time': start_service_time - arrival_time
                }

                if probability_simulation:
                    base_event_data['Arrival Probability'] = arrival_prob
                    base_event_data['Completion Probability'] = completion_prob

                new_data.append(base_event_data)

        return pd.DataFrame(new_data)
