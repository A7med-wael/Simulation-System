from flask import Flask, render_template, request, jsonify, send_file
from services import DataService, SimulationService, PlotService

app = Flask(__name__)
app.secret_key = 'your_secret_key'

data_service = DataService()
simulation_service = SimulationService()
plot_service = PlotService()

@app.route('/')
def index():
    return render_template('index.html', services=data_service.services, current_data=data_service.current_data.to_dict('records'))

@app.route('/add_service', methods=['POST'])
def add_service():
    return data_service.add_service(request.form['service_code'], request.form['service_title'], int(request.form['service_duration']))

@app.route('/simulate', methods=['POST'])
def simulate_customers():
    data_service.current_data = simulation_service.simulate_customers(data_service.services)
    return jsonify({'success': True, 'events': data_service.current_data.to_dict('records')})

@app.route('/arrival_plot.png')
def arrival_plot_png():
    return send_file(plot_service.generate_arrival_and_service_times_plot(data_service.current_data), mimetype='image/png')

@app.route('/customers_system_plot.png')
def customers_system_plot_png():
    return send_file(plot_service.generate_customers_in_system_plot(data_service.current_data), mimetype='image/png')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    return data_service.upload_services_from_file(request.files['file'])

@app.route('/download_data')
def download_data():
    return data_service.download_data()

@app.route('/clear_data')
def clear_data():
    return data_service.clear_data()

if __name__ == '__main__':
    app.run(debug=True)
