from io import BytesIO

import numpy as np
import pandas as pd
from flask import jsonify, url_for

from .interfaces.i_data_service import IDataService


class DataService(IDataService):
    def __init__(self):
        self.services = {}
        self.current_data = pd.DataFrame(columns=[
            'Customer ID', 'Event Type', 'Clock Time',
            'Service Code', 'Service Title', 'Service Duration', 'End Time'
        ])
        self.arrivals = pd.DataFrame(columns=[
            'Time Between Arrival', 'Probability', 'Accumulative Probability',
            'Digit Assignment From', 'Digit Assignment To'
        ])
        self.servers = pd.DataFrame(columns=[
            'Server No.', 'Service Time', 'Server Probability',
            'Server Accumulative Probability', 'Server Digit Assignment From', 'Server Digit Assignment To'
        ])
        self.simulation_servers = pd.DataFrame(columns=[
            'Customer ID', 'Server', 'Arrival Time', 'Wait Time', 'Service Start',
            'Service Duration', 'Service End', 'System End'
        ])

    def add_service(self, code, title, duration):
        if not code or not title or duration <= 0:
            raise ValueError("Invalid service details.")
        if code in self.services:
            raise ValueError(f"Service code '{code}' already exists.")
        self.services[code] = {'title': title, 'duration': duration}
        return jsonify({'success': True, 'service_code': code, 'service_title': title, 'service_duration': duration})

    def validate_numeric_data(self, *values):
        """Utility method to validate numeric values."""
        for value in values:
            if not isinstance(value, (int, float)) or value <= 0:
                raise ValueError(f"Invalid numeric value: {value}")

    def add_arrival(self, time_between_arrivals, probability, accumulative_time, digit_assignment_from, digit_assignment_to):
        """Add an arrival event with a time and probability."""
        self.validate_numeric_data(time_between_arrivals, probability, accumulative_time, digit_assignment_from, digit_assignment_to)
        new_arrival = pd.DataFrame([[time_between_arrivals, probability, accumulative_time, digit_assignment_from, digit_assignment_to]], columns=self.arrivals.columns)
        self.arrivals = pd.concat([self.arrivals, new_arrival], ignore_index=True)
        return jsonify({'success': True, 'events': self.arrivals.to_dict('records')})

    def add_server(self, server_no, service_time, probability, accumulative_time, digit_assignment_from, digit_assignment_to):
        """Add a server with a service time and probability."""
        self.validate_numeric_data(server_no, service_time, probability, accumulative_time, digit_assignment_from, digit_assignment_to)
        new_server = pd.DataFrame([[server_no, service_time, probability, accumulative_time, digit_assignment_from, digit_assignment_to]], columns=self.servers.columns)
        self.servers = pd.concat([self.servers, new_server], ignore_index=True)
        return jsonify({'success': True, 'events': self.servers.to_dict('records')})

    def upload_services_from_file(self, file):
        df = pd.read_excel(file) if file.filename.endswith('.xlsx') else pd.read_csv(file)
        if 'Service Code' not in df.columns or 'Service Title' not in df.columns or 'Service Duration (minutes)' not in df.columns:
            raise ValueError("Invalid file format.")
        self.services = {
            row['Service Code']: {'code': row['Service Code'], 'title': row['Service Title'], 'duration': row['Service Duration (minutes)']}
            for _, row in df.iterrows() if not pd.isna(row['Service Code'])
        }
        return jsonify({'success': True, 'message': f'{len(self.services)} services loaded', 'data': list(self.services.values())})

    def upload_data_from_file(self, file):
        """Upload arrival and server data from an Excel or CSV file."""
        try:
            df = pd.read_excel(file) if file.filename.endswith('.xlsx') else pd.read_csv(file)

            # Clean up the column names and drop unnamed columns
            df.columns = df.columns.str.strip()  # Remove leading/trailing whitespace
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Drop unnamed columns

            # Validate arrival columns and update arrivals data
            arrival_cols = self.arrivals.columns
            if all(col in df.columns for col in arrival_cols):
                self.arrivals = df[arrival_cols].dropna().copy()

            # Validate server columns and update servers data
            server_cols = self.servers.columns
            if all(col in df.columns for col in server_cols):
                self.servers = df[server_cols].dropna().copy()
            else:
                # Create a new DataFrame for servers if not all columns are provided
                missing_cols = set(server_cols) - set(df.columns)
                if missing_cols == {'Server No.'}:
                    # If only Server No. is missing, add it with random values between 1 and 10
                    df['Server No.'] = np.random.randint(1, 11, size=len(df))  # Random integers between 1 and 10
                    self.servers = df[server_cols].dropna().copy()
                else:
                    # Handle case where other server columns are also missing
                    raise ValueError(f"Missing server columns: {', '.join(missing_cols)}")

            return jsonify({
                'success': True,
                'message': 'Data uploaded successfully!',
                'arrivals': self.arrivals.to_dict('records'),
                'servers': self.servers.to_dict('records')
            })
        except Exception as e:
            return jsonify({'success': False, 'message': f"Failed to upload data: {str(e)}"})

    def clear_data(self):
        self.current_data = pd.DataFrame(columns=self.current_data.columns)
        self.services.clear()
        return jsonify({'success': True, 'message': 'All data cleared successfully!'})

    def clear_parallel_data(self):
        """Clear arrival and server data."""
        self.arrivals = self.arrivals.iloc[0:0]
        self.servers = self.servers.iloc[0:0]
        return jsonify({'success': True, 'message': 'All data cleared successfully!'})

    def download_data(self):
        if self.current_data.empty:
            return jsonify({'success': False, 'message': 'No data available to download'})

        try:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                self.current_data.to_excel(writer, sheet_name='Queue Data', index=False)
            output.seek(0)

            file_path = 'static/temp/queue_data.xlsx'
            with open(file_path, 'wb') as f:
                f.write(output.read())

            return jsonify({
                'success': True,
                'file_url': url_for('static', filename='temp/queue_data.xlsx')
            })

        except Exception as e:
            return jsonify({'success': False, 'message': f'Error downloading data: {str(e)}'})

    def download_parallel_data(self):
        """Download arrival and server data to an Excel file with multiple sheets."""
        if self.arrivals.empty and self.servers.empty:
            return jsonify({'success': False, 'message': 'No data available to download'})

        try:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                if not self.arrivals.empty:
                    self.arrivals.to_excel(writer, sheet_name='Arrival Probability', index=False)
                if not self.servers.empty:
                    self.servers.to_excel(writer, sheet_name='Server Probability', index=False)

            output.seek(0)
            file_path = 'static/temp/parallel_queue_data.xlsx'
            with open(file_path, 'wb') as f:
                f.write(output.read())

            return jsonify({
                'success': True,
                'file_url': url_for('static', filename='temp/parallel_queue_data.xlsx')
            })
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error downloading data: {str(e)}'})