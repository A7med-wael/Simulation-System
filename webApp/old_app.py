""" 
import random
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize services and customer data
services = {}
current_data = pd.DataFrame(columns=[
    'Customer ID', 'Event Type', 'Clock Time',
    'Service Code', 'Service Title', 'Service Duration', 'End Time'
])

@app.route('/')
def index():
    """"""Render the home page.""""""
    return render_template('index.html', services=services, current_data=current_data.to_dict('records'))

@app.route('/add_service', methods=['POST'])
def add_service():
    """"""Handle adding a new service.""""""
    try:
        code = request.form['service_code'].strip()
        title = request.form['service_title'].strip()
        duration = int(request.form['service_duration'].strip())

        if not code or not title or duration <= 0:
            raise ValueError("Please provide valid service details.")

        if code in services:
            raise ValueError(f"Service code '{code}' already exists.")

        services[code] = {'title': title, 'duration': duration}
        return jsonify({'success': True, 'service_code': code, 'service_title': title, 'service_duration': duration})

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/simulate', methods=['POST'])
def simulate_customers():
    """"""Generate random customer data.""""""
    global current_data

    if not services:
        return jsonify({'success': False, 'error': 'No services available! Please add services first.'})

    try:
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

        current_data = pd.DataFrame(new_data)
        return jsonify({'success': True, 'events': new_data})

    except Exception as e:
        return jsonify({'success': False, 'error': f'Error generating customers: {str(e)}'})

@app.route('/plot.png')
def plot_png():
    """"""Generate a matplotlib graph and return it as an image.""""""
    fig, ax = plt.subplots(figsize=(12, 6))

    # Check if there is data to plot
    if not current_data.empty:
        try:
            # Sort data by 'Clock Time' for accurate plotting
            sorted_data = current_data.sort_values('Clock Time')

            # Calculate the cumulative number of customers in the system
            sorted_data['Count Change'] = sorted_data['Event Type'].map({'Arrival': 1, 'Departure': -1})
            sorted_data['Customers in System'] = sorted_data['Count Change'].cumsum()

            # Plot a step graph
            ax.step(sorted_data['Clock Time'], sorted_data['Customers in System'], where='post', color='blue',
                    label='Customers in System')

            # Add annotations for each event
            prev_y = 0
            y_offset = 0
            for _, row in sorted_data.iterrows():
                current_y = row['Customers in System']

                # Adjust y_offset to avoid overlapping text
                if abs(current_y - prev_y) < 0.1:
                    y_offset = (y_offset + 0.2) % 0.6
                else:
                    y_offset = 0

                # Annotate each point with customer ID and event type (Arrival/Departure)
                ax.annotate(
                    f"C{row['Customer ID']}\n{row['Event Type'][0]}",
                    (row['Clock Time'], row['Customers in System'] + y_offset),
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                    fontsize=8
                )
                prev_y = current_y

            # Configure graph settings
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_xlabel('Clock Time')
            ax.set_ylabel('Customers in System')
            ax.set_title('System State Over Time')
            ax.legend()

            # Adjust y-axis limits to prevent clipping of annotations
            y_min, y_max = ax.get_ylim()
            ax.set_ylim(y_min, y_max + 1)

        except Exception as e:
            # Optional: add a flash message or logging here
            print(f"Error updating graph: {e}")

    else:
        # Display a placeholder if there is no data
        ax.text(0.5, 0.5, 'No data to display', horizontalalignment='center', verticalalignment='center')
        ax.set_xticks([])
        ax.set_yticks([])

    # Save the figure to a BytesIO object and send it as an image response
    output = BytesIO()
    plt.savefig(output, format='png')
    plt.close(fig)
    output.seek(0)
    return send_file(output, mimetype='image/png')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    """"""Handle file upload for services data.""""""
    file = request.files.get('file')

    if not file:
        flash('No file uploaded', 'danger')
        return redirect(url_for('index'))

    try:
        df = pd.read_excel(file) if file.filename.endswith('.xlsx') else pd.read_csv(file)
        required_columns = ['Service Code', 'Service Title', 'Service Duration (minutes)']

        if not all(col in df.columns for col in required_columns):
            raise ValueError("Invalid file format. Columns required: 'Service Code', 'Service Title', 'Service Duration (minutes)'.")

        global services
        services.clear()

        for _, row in df.iterrows():
            if not pd.isna(row['Service Code']):
                services[str(row['Service Code'])] = {
                    'code': str(row['Service Code']),
                    'title': str(row['Service Title']),
                    'duration': int(row['Service Duration (minutes)'])
                }

        return jsonify({'success': True, 'message': f'Successfully loaded {len(services)} services!',
                        'data': list(services.values())})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Failed to load file: {str(e)}'})

@app.route('/download_data')
def download_data():
    """"""Download current customer data as an Excel file.""""""
    global current_data
    if current_data.empty:
        flash('No data available to download', 'danger')
        return redirect(url_for('index'))

    try:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            current_data.to_excel(writer, sheet_name='Queue Data', index=False)

        output.seek(0)
        return send_file(output, as_attachment=True, download_name='queue_data.xlsx')

    except Exception as e:
        flash(f'Error downloading data: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/clear_data')
def clear_data():
    """"""Clear all current data.""""""
    global current_data, services
    current_data = pd.DataFrame(columns=[
        'Customer ID', 'Event Type', 'Clock Time',
        'Service Code', 'Service Title', 'Service Duration', 'End Time'
    ])
    services.clear()
    return jsonify({'success': True, 'message': 'All data cleared successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
"""