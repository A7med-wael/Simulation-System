import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:simulator_app/constents.dart';
import 'package:simulator_app/methodes/add_service.dart';
import 'package:simulator_app/methodes/clear_all_data.dart';
import 'package:simulator_app/methodes/simulate_one_serever.dart';
import 'package:simulator_app/methodes/initialize_data.dart';
import 'package:simulator_app/methodes/probability_simulation.dart';
import 'package:simulator_app/methodes/save_all_data.dart';
import 'package:simulator_app/methodes/simulate_two_serever.dart';
import 'package:simulator_app/models/customer_event.dart';
import 'package:simulator_app/widgets/action_buttons.dart';
import 'package:simulator_app/widgets/build_chronological_events_table.dart';
import 'package:simulator_app/widgets/build_customer_data_table.dart';
import 'package:simulator_app/widgets/custom_button.dart';
import 'package:simulator_app/widgets/service_form.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController serviceCodeController = TextEditingController();
  final TextEditingController serviceTitleController = TextEditingController();
  final TextEditingController serviceDurationController =
      TextEditingController();

  List<Map<String, dynamic>> newData = [];
  List<CustomerEvent> currentData = [];
  Map<String, Map<String, dynamic>> services = {};
  List<CustomerEvent> simulatedData = [];
  List<FlSpot> graphDataPoints = [];
  bool showProbabilityColumns = false;
  bool showParallelColumns = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // backgroundColor: Color.fromARGB(255, 108, 140, 156),
      backgroundColor: PrimaryColor,
      appBar: AppBar(
        iconTheme: IconThemeData(color: Colors.white),
        forceMaterialTransparency: true,
        elevation: 0,
        backgroundColor: PrimaryColor,
        title: const Text(
          'Simulation Overview',
          style: TextStyle(
            color: Colors.white,
            fontSize: 25,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(
                color: PrimaryColor,
              ),
              child: Text(
                'Can not serve mysilf',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            buildServerExpansionTile(
              title: 'Single Server',
              onSimulate: () => simulateOneServer(
                services: services,
                currentData: currentData,
                context: context,
                updateDisplays: updateDisplays,
              ),
            ),
            buildServerExpansionTile(
              title: 'Parallel Server',
              onSimulate: () => simulateTwoServers(
                services: services,
                currentData: currentData,
                context: context,
                updateDisplays: updateDisplays,
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 16.0),
              child: Column(
                children: [
                  CustomButton(
                    onPressed: () => saveAllData(
                      currentData: currentData,
                      context: context,
                    ),
                    text: 'Save Data',
                  ),
                  CustomButton(
                    onPressed: () => clearAllData(
                      services: services,
                      currentData: currentData,
                      context: context,
                      newData: newData,
                      graphDataPoints: graphDataPoints,
                      updateDisplays: updateDisplays,
                    ),
                    text: 'Clear Data',
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
              colors: [
                // Color.fromARGB(255, 108, 140, 156),
                // Color.fromARGB(255, 172, 199, 212)
                // Colors.red, Colors.green
                Color(0xff022b3a),
                Color(0xff1f7a8c),
              ],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              stops: [.00001, .5]),
          borderRadius: BorderRadius.circular(20), // Rounded corners
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.1),
              offset: Offset(0, 5),
              blurRadius: 15,
              spreadRadius: 2,
            ),
          ],
        ),
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 16),
              Expanded(
                child: ClipRRect(
                  borderRadius:
                      BorderRadius.circular(15), // Rounded inner widgets
                  child: ListView(
                    children: [
                      buildSectionHeader('Customer Data Table'),
                      const SizedBox(height: 10),
                      buildCustomerDataTable(
                        newData: newData,
                        showProbabilityColumns: showProbabilityColumns,
                        showParallelColumns: showParallelColumns,
                      ),
                      const SizedBox(height: 20),
                      buildSectionHeader('Chronological Events'),
                      const SizedBox(height: 10),
                      buildChronologicalEventsTable(
                        currentData: currentData,
                        showProbabilityColumns: showProbabilityColumns,
                      ),
                      const SizedBox(height: 40),
                      buildSectionHeader('Graph Display'),
                      const SizedBox(height: 10),
                      buildGraphDisplay(),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget buildSectionHeader(String title) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.8),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            offset: Offset(0, 3),
            blurRadius: 8,
          ),
        ],
      ),
      child: Text(
        title,
        style: const TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: Color.fromARGB(255, 60, 90, 110),
        ),
      ),
    );
  }

  void updateDisplays() {
    graphDataPoints = [];
    double offset = 0.5;

    for (var event in currentData) {
      if (event.eventType == "Arrival") {
        double yValue = double.parse(event.customerId);
        double startXValue = (double.tryParse(event.clockTime) ?? 0.0) +
            (offset * int.parse(event.customerId));
        double endXValue = (double.tryParse(event.endTime) ?? 0.0) +
            (offset * int.parse(event.customerId));

        graphDataPoints.add(FlSpot(startXValue, yValue));
        graphDataPoints.add(FlSpot(endXValue, yValue));
      }
    }

    newData = currentData.map((event) {
      return {
        'Customer ID': event.customerId,
        'Event Type': event.eventType,
        'Clock Time': event.clockTime,
        'Service Code': event.serviceCode,
        'Service Title': event.serviceTitle,
        'Service Duration': event.serviceDuration,
        'End Time': event.endTime,
        'Server': event.server,
        'Arrival Probability': event.arrivalProb,
        'Completion Probability': event.completionProb,
      };
    }).toList();

    setState(() {});
  }

  Widget buildGraphDisplay() {
    return Container(
      // padding: EdgeInsets.symmetric(vertical: 8),
      // margin: EdgeInsets.symmetric(vertical: 8),
      height: 320,
      decoration: BoxDecoration(
        color: Colors.grey[200],
        borderRadius: BorderRadius.circular(10),
      ),
      child: LineChart(
        LineChartData(
          lineBarsData: [
            LineChartBarData(
              spots: graphDataPoints,
              isCurved: true,
              gradient: const LinearGradient(
                colors: [Colors.blueAccent, Colors.lightBlue],
              ),
              belowBarData: BarAreaData(
                show: true,
                gradient: LinearGradient(
                  colors: [
                    Colors.blueAccent.withOpacity(0.3),
                    Colors.lightBlue.withOpacity(0.0),
                  ],
                ),
              ),
              dotData: FlDotData(
                show: true,
                getDotPainter: (spot, percent, barData, index) {
                  return FlDotCirclePainter(
                    radius: 4,
                    color: Colors.redAccent,
                    strokeWidth: 2,
                    strokeColor: Colors.blueAccent,
                  );
                },
              ),
              isStrokeCapRound: true,
              barWidth: 3,
            ),
          ],
          gridData: FlGridData(
            show: true,
            drawVerticalLine: true,
            verticalInterval: 1,
            horizontalInterval: 1,
            getDrawingVerticalLine: (value) => FlLine(
              color: Colors.grey.withOpacity(0.3),
              strokeWidth: 1,
            ),
            getDrawingHorizontalLine: (value) => FlLine(
              color: Colors.grey.withOpacity(0.3),
              strokeWidth: 1,
            ),
          ),
          titlesData: FlTitlesData(
            show: true,
            bottomTitles: AxisTitles(
              sideTitles: SideTitles(showTitles: true),
            ),
            leftTitles: AxisTitles(
              sideTitles: SideTitles(showTitles: true),
            ),
          ),
        ),
      ),
    );
  }

  Widget buildServerExpansionTile({
    required String title,
    required VoidCallback onSimulate,
  }) {
    return ExpansionTile(
      title: Text(
        title,
        style: const TextStyle(fontWeight: FontWeight.bold),
      ),
      leading: const Icon(Icons.touch_app),
      children: [
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            children: [
              buildActionButtons(
                onUploadFile: () {
                  initializeData(
                    context: context,
                    services: services,
                    onSuccess: () {},
                  );
                },
                onSimulate: onSimulate,
                onProbability: () {
                  showProbabilityColumns = true;
                  probabilitySimulation(
                    services: services,
                    currentData: currentData,
                    context: context,
                    updateDisplays: updateDisplays,
                  );
                },
              ),
              const SizedBox(height: 30),
              buildServiceForm(
                codeController: serviceCodeController,
                titleController: serviceTitleController,
                durationController: serviceDurationController,
                onAddService: () {
                  addService(
                    serviceCodeController: serviceCodeController,
                    serviceTitleController: serviceTitleController,
                    serviceDurationController: serviceDurationController,
                    services: services,
                  );
                },
              ),
            ],
          ),
        ),
      ],
    );
  }
}
