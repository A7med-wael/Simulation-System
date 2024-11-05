import random
from datetime import timedelta

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

    def simulate_parallel_servers(self, servers_data, arrivals_data):
        """Simulate customer arrivals and service times for parallel servers."""

        # Check if the DataFrames are empty
        if servers_data.empty or arrivals_data.empty:
            return jsonify(
                {'success': False, 'error': 'Please ensure both arrival and server probability tables have data.'})

        simulation_period = timedelta(hours=1)
        servers = {
            'Able': {'available_from': timedelta(0), 'service_times': []},
            'Baker': {'available_from': timedelta(0), 'service_times': []}
        }

        customers = []
        arrival_time = timedelta(0)

        def get_time_from_probability_table(random_value_, probability_table, key_name):
            expected_key = 'Accumulative Probability' if 'Accumulative Probability' in probability_table.columns else 'Server Accumulative Probability'
            print(probability_table.columns)
            for index, row in probability_table.iterrows():
                if random_value_ <= row[expected_key]:
                    return row[key_name]
            raise ValueError(f"No matching entry found in the probability table for random value: {random_value_}")

        # Main simulation loop for customer arrivals and service
        while arrival_time < simulation_period:
            random_value = random.random()
            time_between_arrivals = get_time_from_probability_table(random_value, arrivals_data, 'Time Between Arrival')
            arrival_time += timedelta(minutes=time_between_arrivals)

            # Determine the assigned server
            assigned_server = self.assign_server(servers, arrival_time)

            random_value = random.random()
            service_time = get_time_from_probability_table(random_value, servers_data, 'Service Time')

            start_time = max(arrival_time, servers[assigned_server]['available_from'])
            end_time = start_time + timedelta(minutes=service_time)

            # Construct customer record
            customer_info = {
                'Customer ID': len(customers) + 1,
                'Clock Time': arrival_time.total_seconds() / 60,
                'Event Type': 'Arrival',
                'Service Duration': service_time,
                'End Time': end_time.total_seconds() / 60,
                'Server': assigned_server,
                'Wait Time': (start_time - arrival_time).total_seconds() / 60,
                'Service Time': service_time
            }
            customers.append(customer_info)

            # Update server availability and service time
            servers[assigned_server]['available_from'] = end_time
            servers[assigned_server]['service_times'].append(service_time)

        # Create DataFrame and metrics
        df_customers = pd.DataFrame(customers)
        metrics = self.calculate_metrics(df_customers, servers, simulation_period)

        return df_customers, metrics

    def assign_server(self, servers, arrival_time):
        """Assign the server based on availability and service time."""
        if servers['Able']['available_from'] <= arrival_time:
            return 'Able'
        elif servers['Baker']['available_from'] <= arrival_time:
            return 'Baker'
        else:
            return 'Able' if servers['Able']['available_from'] < servers['Baker']['available_from'] else 'Baker'

    def calculate_metrics(self, df_customers, servers, simulation_period):
        """Calculate performance metrics for the servers."""
        total_simulation_time = simulation_period.total_seconds() / 60
        able_busy_time = min(sum(servers['Able']['service_times']), total_simulation_time)
        baker_busy_time = min(sum(servers['Baker']['service_times']), total_simulation_time)

        metrics = {
            'Able Utilization Rate': f"{min(able_busy_time / total_simulation_time, 1.0):.2%}",
            'Baker Utilization Rate': f"{min(baker_busy_time / total_simulation_time, 1.0):.2%}",
            'Average Waiting Time': f"{df_customers['Wait Time'].mean():.2f} minutes",
            'Total Customers': len(df_customers)
        }
        return metrics
