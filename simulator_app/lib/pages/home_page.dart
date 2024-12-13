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
import 'package:flutter/src/painting/box_border.dart' as box_border;

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
      appBar: AppBar(
        backgroundColor: PrimaryColor,
        title: const Text(
          'Simulation Clock Table',
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
                'Menu',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 30,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            ExpansionTile(
              title: const Text(
                'single server',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              leading: const Icon(Icons.touch_app),
              children: [
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    children: [
                      buildActionButtons(onUploadFile: () {
                        initializeData(
                            context: context,
                            services: services,
                            onSuccess: () {});
                      }, onSimulate: () {
                        simulateOneServer(
                            services: services,
                            currentData: currentData,
                            context: context,
                            updateDisplays: updateDisplays);
                      }, onProbability: () {
                        showProbabilityColumns = true;
                        probabilitySimulation(
                          services: services,
                          currentData: currentData,
                          context: context,
                          updateDisplays: updateDisplays,
                        );
                      }),
                      const SizedBox(height: 30),
                      buildServiceForm(
                          codeController: serviceCodeController,
                          titleController: serviceTitleController,
                          durationController: serviceDurationController,
                          onAddService: () {
                            addService(
                              serviceCodeController: serviceCodeController,
                              serviceTitleController: serviceTitleController,
                              serviceDurationController:
                                  serviceDurationController,
                              services: services,
                            );
                          }),
                    ],
                  ),
                ),
              ],
            ),
            ExpansionTile(
              title: const Text(
                'parallel server',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              leading: const Icon(Icons.touch_app),
              children: [
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    children: [
                      buildActionButtons(onUploadFile: () {
                        initializeData(
                            context: context,
                            services: services,
                            onSuccess: () {});
                      }, onSimulate: () {
                        showParallelColumns = true;
                        simulateTwoServers(
                            services: services,
                            currentData: currentData,
                            context: context,
                            updateDisplays: updateDisplays);
                      }, onProbability: () {
                        showProbabilityColumns = true;
                        probabilitySimulation(
                          services: services,
                          currentData: currentData,
                          context: context,
                          updateDisplays: updateDisplays,
                        );
                      }),
                      const SizedBox(height: 30),
                      buildServiceForm(
                          codeController: serviceCodeController,
                          titleController: serviceTitleController,
                          durationController: serviceDurationController,
                          onAddService: () {
                            addService(
                              serviceCodeController: serviceCodeController,
                              serviceTitleController: serviceTitleController,
                              serviceDurationController:
                                  serviceDurationController,
                              services: services,
                            );
                          }),
                    ],
                  ),
                ),
              ],
            ),
            SizedBox(height: MediaQuery.of(context).size.height * 0.49),
            Column(
              children: [
                CustomButton(
                    onPressed: () {
                      saveAllData(currentData: currentData, context: context);
                    },
                    text: 'Save Data'),
                CustomButton(
                    onPressed: () {
                      clearAllData(
                          services: services,
                          currentData: currentData,
                          context: context,
                          newData: newData,
                          graphDataPoints: graphDataPoints,
                          updateDisplays: updateDisplays);
                    },
                    text: 'Clear Data'),
              ],
            ),
          ],
        ),
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color.fromARGB(255, 108, 140, 156), Colors.white],
            begin: Alignment.topRight,
            end: Alignment.bottomLeft,
          ),
        ),
        child: Center(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
            child: ListView(
              children: [
                const SizedBox(height: 20),
                buildCustomerDataTable(
                  newData: newData,
                  showProbabilityColumns: showProbabilityColumns,
                  showParallelColumns: showParallelColumns,
                ),
                const SizedBox(height: 20),
                buildChronologicalEventsTable(
                    currentData: currentData,
                    showProbabilityColumns: showProbabilityColumns),
                const SizedBox(height: 40),
                buildGraphDisplay(),
              ],
            ),
          ),
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
      height: 300, // Adjust as needed for visibility
      width: double.infinity,
      decoration: BoxDecoration(
        color: Colors.grey[200], // Subtle background color
        borderRadius: BorderRadius.circular(10),
      ),
      child: LineChart(
        LineChartData(
          lineBarsData: [
            LineChartBarData(
              spots: graphDataPoints,
              isCurved: true, // Add smooth curves
              gradient: const LinearGradient(
                colors: [Colors.blueAccent, Colors.lightBlue],
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
              ), // Apply gradient to the line
              belowBarData: BarAreaData(
                show: true,
                gradient: LinearGradient(
                  colors: [
                    Colors.blueAccent.withOpacity(0.3),
                    Colors.lightBlue.withOpacity(0.0)
                  ],
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                ),
              ), // Show gradient fill below the line
              dotData: FlDotData(
                show: true,
                getDotPainter: (spot, percent, barData, index) {
                  return FlDotCirclePainter(
                    radius: 4,
                    color: Colors.redAccent, // Customize dot color
                    strokeWidth: 2,
                    strokeColor: Colors.blueAccent,
                  );
                },
              ),
              isStrokeCapRound: true,
              barWidth: 3, // Thicker line width
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
              dashArray: [5, 5], // Dashed vertical lines
            ),
            getDrawingHorizontalLine: (value) => FlLine(
              color: Colors.grey.withOpacity(0.3),
              strokeWidth: 1,
              dashArray: [5, 5], // Dashed horizontal lines
            ),
          ),
          titlesData: FlTitlesData(
            leftTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                reservedSize: 30,
                getTitlesWidget: (value, meta) {
                  return Padding(
                    padding: const EdgeInsets.only(right: 8.0),
                    child: Text(
                      value.toInt().toString(),
                      style: const TextStyle(color: Colors.blueAccent),
                    ),
                  ); // Display customer ID on the y-axis
                },
              ),
            ),
            bottomTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                reservedSize: 30,
                getTitlesWidget: (value, meta) {
                  return Padding(
                    padding: const EdgeInsets.only(top: 8.0),
                    child: Text(
                      value.toInt().toString(),
                      style: const TextStyle(color: Colors.blueAccent),
                    ),
                  ); // Display clock time on the x-axis
                },
              ),
            ),
            topTitles: AxisTitles(
              sideTitles: SideTitles(showTitles: false),
            ),
            rightTitles: AxisTitles(
              sideTitles: SideTitles(showTitles: false),
            ),
          ),
          borderData: FlBorderData(
            show: true,
            border: box_border.Border.all(
              color: Colors.blueAccent,
              width: 1,
            ),
          ),
        ),
      ),
    );
  }
}
