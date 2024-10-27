from io import BytesIO

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

    def add_service(self, code, title, duration):
        if not code or not title or duration <= 0:
            raise ValueError("Invalid service details.")
        if code in self.services:
            raise ValueError(f"Service code '{code}' already exists.")
        self.services[code] = {'title': title, 'duration': duration}
        return jsonify({'success': True, 'service_code': code, 'service_title': title, 'service_duration': duration})

    def upload_services_from_file(self, file):
        df = pd.read_excel(file) if file.filename.endswith('.xlsx') else pd.read_csv(file)
        if 'Service Code' not in df.columns or 'Service Title' not in df.columns or 'Service Duration (minutes)' not in df.columns:
            raise ValueError("Invalid file format.")
        self.services = {
            row['Service Code']: {'code': row['Service Code'], 'title': row['Service Title'], 'duration': row['Service Duration (minutes)']}
            for _, row in df.iterrows() if not pd.isna(row['Service Code'])
        }
        return jsonify({'success': True, 'message': f'{len(self.services)} services loaded', 'data': list(self.services.values())})

    def clear_data(self):
        self.current_data = pd.DataFrame(columns=self.current_data.columns)
        self.services.clear()
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