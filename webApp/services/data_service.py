from io import BytesIO

import numpy as np
import pandas as pd
from flask import jsonify, url_for

from .interfaces.i_data_service import IDataService


class DataService(IDataService):
    def __init__(self):
        self.counter = 0
        self.prev_arr = 0
        self.services = {}
        self.current_data = pd.DataFrame(columns=[
            'Customer ID', 'Event Type', 'Interval Time', 'Clock Time',
            'Service Code', 'Service Title', 'Service Duration', 'End Time', 'Start Time'
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
        self.counter += 1
        return jsonify({'success': True, 'service_code': code, 'service_title': title, 'service_duration': duration})
        

    def validate_numeric_data(self, *values):
        """Utility method to validate numeric values."""
        for value in values:
            if not isinstance(value, (int, float)) or value <= 0:
                raise ValueError(f"Invalid numeric value: {value}")

    def add_data(self, crt_arr, service_time, server_no):
        """Add a single arrival or server entry and recalculate probabilities."""
        time_between_arrivals = self.prev_arr + crt_arr
        self.prev_arr = crt_arr

        new_arrival = pd.DataFrame([{
            "Time Between Arrival": time_between_arrivals,
            "Probability": 0,
            "Accumulative Probability": 0,
            "Digit Assignment From": 0,
            "Digit Assignment To": 0
        }])
        self.arrivals = pd.concat([self.arrivals, new_arrival], ignore_index=True)

        total_time = self.arrivals["Time Between Arrival"].sum()
        temp_accum = 0
        for idx, row in self.arrivals.iterrows():
            prob = row["Time Between Arrival"] / total_time
            accum_prob = temp_accum + prob
            digit_from = int(temp_accum * 100)
            digit_to = 100 if idx == len(self.arrivals) - 1 else int(accum_prob * 100) - 1

            self.arrivals.at[idx, "Probability"] = round(prob, 2)
            self.arrivals.at[idx, "Accumulative Probability"] = round(accum_prob, 2)
            self.arrivals.at[idx, "Digit Assignment From"] = digit_from
            self.arrivals.at[idx, "Digit Assignment To"] = digit_to

            temp_accum = accum_prob

        new_server = pd.DataFrame([{
            "Server No.": server_no,
            "Service Time": service_time
        }])
        self.servers = pd.concat([self.servers, new_server], ignore_index=True)

        total_service_time = self.servers["Service Time"].sum()
        temp_accum = 0
        for idx, row in self.servers.iterrows():
            prob = row["Service Time"] / total_service_time
            accum_prob = temp_accum + prob
            digit_from = int(temp_accum * 100)
            digit_to = 100 if idx == len(self.servers) - 1 else int(accum_prob * 100) - 1

            self.servers.at[idx, "Server Probability"] = round(prob, 2)
            self.servers.at[idx, "Server Accumulative Probability"] = round(accum_prob, 2)
            self.servers.at[idx, "Server Digit Assignment From"] = digit_from
            self.servers.at[idx, "Server Digit Assignment To"] = digit_to

            temp_accum = accum_prob

        return jsonify({
            'success': True,
            'events': {
                "arrivals": self.arrivals.to_dict('records'),
                "servers": self.servers.to_dict('records')
            }
        })

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

            df.columns = df.columns.str.strip()
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            arrival_cols = self.arrivals.columns
            if all(col in df.columns for col in arrival_cols):
                self.arrivals = df[arrival_cols].dropna().copy()

            server_cols = self.servers.columns
            if all(col in df.columns for col in server_cols):
                self.servers = df[server_cols].dropna().copy()
            else:
                missing_cols = set(server_cols) - set(df.columns)
                if missing_cols == {'Server No.'}:
                    df['Server No.'] = np.random.randint(1, 11, size=len(df))
                    self.servers = df[server_cols].dropna().copy()
                else:
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
        self.arrivals = pd.DataFrame(columns=self.arrivals.columns)
        self.servers = pd.DataFrame(columns=self.servers.columns)
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