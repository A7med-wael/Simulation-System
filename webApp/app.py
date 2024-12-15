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
    probability_simulation = request.json.get('probability_simulation', False)
    data_service.current_data = simulation_service.simulate_customers(data_service.services, probability_simulation)
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

# Parallel server routes
@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.form
    crt_arr = int(data.get('crt_arr'))
    service_time = int(data.get('service_time'))
    server_name = int(data.get('server_no'))
    return data_service.add_data(crt_arr, service_time, server_name)

@app.route('/simulate_servers', methods=['POST'])
def simulate_servers():
    df_customers, metrics = simulation_service.simulate_parallel_servers(data_service.servers, data_service.arrivals)
    data_service.simulation_servers = df_customers

    return jsonify({
        'success': True,
        'events': df_customers.to_dict('records'),
        'metrics': metrics
    })

@app.route('/upload_file_parallel', methods=['POST'])
def upload_file_parallel():
    file = request.files['file']
    return data_service.upload_data_from_file(file)

@app.route('/download_parallel_data')
def download_parallel_data():
    return data_service.download_parallel_data()

@app.route('/clear_data_parallel')
def clear_data_parallel():
    return data_service.clear_parallel_data()

@app.route('/parallel_servers_plot.png')
def parallel_servers_plot_png():
    plot_image = plot_service.generate_parallel_servers_plot(data_service.simulation_servers)
    return send_file(plot_image, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
