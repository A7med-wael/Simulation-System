import 'dart:math';
import 'dart:io';
import 'package:excel/excel.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:simulator_app/constents.dart';
import 'package:simulator_app/models/customer_event.dart';
import 'package:flutter/src/painting/box_border.dart' as box_border;
import '../widgets/custom_button.dart';

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
  List<FlSpot> graphDataPoints = [];

  bool showProbabilityColumns = false;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _buildAppBar(),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
          child: ListView(
            children: [
              _buildActionButtons(),
              const SizedBox(height: 20),
              _buildServiceForm(),
              const SizedBox(height: 20),
              buildGraphDisplay(),
              const SizedBox(height: 20),
              buildCustomerDataTable(),
              const SizedBox(height: 20),
              buildChronologicalEventsTable(),
            ],
          ),
        ),
      ),
    );
  }

  AppBar _buildAppBar() {
    return AppBar(
      backgroundColor: PrimaryColor,
      title: const Text(
        'Simulation Clock Table',
        style: TextStyle(
          color: Colors.white,
          fontSize: 25,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }

  Widget _buildActionButtons() {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            CustomButton(onPressed: initializeData, text: 'Upload File'),
            CustomButton(
                onPressed: () {
                  setState(() {
                    showProbabilityColumns = false;
                    generateCustomers();
                  });
                },
                text: 'Simulate'),
          ],
        ),
        CustomButton(
            onPressed: () {
              setState(() {
                showProbabilityColumns = true;
                probabilitySimulation();
              });
            },
            text: 'Probability'),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            CustomButton(onPressed: saveAllData, text: 'Save Data'),
            CustomButton(onPressed: clearAllData, text: 'Clear Data'),
          ],
        ),
      ],
    );
  }

  Widget _buildServiceForm() {
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Center(
            child: Text('Add New Service',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
          ),
          const SizedBox(height: 10),
          _buildTextInputField(
              controller: serviceCodeController, labelText: 'Service Code:'),
          _buildTextInputField(
              controller: serviceTitleController, labelText: 'Service Title:'),
          _buildTextInputField(
              controller: serviceDurationController,
              labelText: 'Duration (min):',
              keyboardType: TextInputType.number),
          const SizedBox(height: 10),
          Center(
            child: CustomButton(
              onPressed: _addService,
              text: 'Add Service',
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTextInputField({
    required TextEditingController controller,
    required String labelText,
    TextInputType keyboardType = TextInputType.text,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: TextFormField(
        controller: controller,
        decoration: InputDecoration(
          labelText: labelText,
          border: const OutlineInputBorder(),
        ),
        keyboardType: keyboardType,
      ),
    );
  }

  Future<void> initializeData() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['xlsx', 'xls'],
    );

    if (result != null && result.files.isNotEmpty) {
      String? filePath = result.files.single.path;
      var file = File(filePath!);
      try {
        var bytes = file.readAsBytesSync();
        var excel = Excel.decodeBytes(bytes);
        for (var table in excel.tables.keys) {
          for (var row in excel.tables[table]!.rows) {
            if (row.isNotEmpty) {
              var serviceCode = row[0]?.value;
              var serviceTitle = row[1]?.value;
              var serviceDuration = row[2]?.value;

              if (serviceCode != null &&
                  serviceTitle != null &&
                  serviceDuration != null) {
                services[serviceCode.toString()] = {
                  'serviceCode': serviceCode.toString(),
                  'serviceTitle': serviceTitle.toString(),
                  'serviceDuration': serviceDuration.toString(),
                };
              }
            }
          }
        }

        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('File Loaded'),
            content: const Text('File loaded successfully.'),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text('OK'),
              ),
            ],
          ),
        );
        print("Services Loaded: $services");
        setState(() {
          updateDisplays();
        });
      } catch (e) {
        print('Error while processing Excel file: $e');
      }
    } else {
      print('No file selected');
    }
  }

  void updateDisplays() {
    graphDataPoints = [];
    double offset = 0.5; // Adjust this value to separate lines visually

    for (var event in currentData) {
      if (event.eventType == "Arrival") {
        double yValue =
            double.parse(event.customerId); // Customer ID for y-axis
        double startXValue = (double.tryParse(event.clockTime) ?? 0.0) +
            (offset * int.parse(event.customerId)); // Arrival time
        double endXValue = (double.tryParse(event.endTime) ?? 0.0) +
            (offset * int.parse(event.customerId)); // Departure time

        // Add start and end points for each service duration
        graphDataPoints.add(FlSpot(startXValue, yValue)); // Start of service
        graphDataPoints.add(FlSpot(endXValue, yValue)); // End of service
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
        'Arrival Probability': event.arrivalProb.substring(0, 5),
        'Completion Probability': event.completionProb.substring(0, 5),
      };
    }).toList();

    setState(() {});
  }

  Widget buildCustomerDataTable() {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: DataTable(
        columns: [
          const DataColumn(label: Text('Customer ID')),
          const DataColumn(label: Text('Event Type')),
          const DataColumn(label: Text('Clock Time')),
          const DataColumn(label: Text('Service Code')),
          const DataColumn(label: Text('Service Title')),
          const DataColumn(label: Text('Service Duration')),
          const DataColumn(label: Text('End Time')),
          if (showProbabilityColumns)
            const DataColumn(
                label: Text('Arrival Probability')), // Show Probability Column
          if (showProbabilityColumns)
            const DataColumn(label: Text('Completion Probability')),
        ],
        rows: newData.map((data) => _buildDataRow(data)).toList(),
      ),
    );
  }

  DataRow _buildDataRow(Map<String, dynamic> data) {
    return DataRow(cells: [
      DataCell(Text(data['Customer ID'].toString())),
      DataCell(Text(data['Event Type'].toString())),
      DataCell(Text(data['Clock Time'].toString())),
      DataCell(Text(data['Service Code'].toString())),
      DataCell(Text(data['Service Title'].toString())),
      DataCell(Text(data['Service Duration'].toString())),
      DataCell(Text(data['End Time'].toString())),
      if (showProbabilityColumns)
        DataCell(Text(data['Arrival Probability'].toString())),
      if (showProbabilityColumns)
        DataCell(Text(data['Completion Probability'].toString())),
    ]);
  }

  Widget buildChronologicalEventsTable() {
    return Padding(
      padding: const EdgeInsets.all(10.0),
      child: Column(
        children: [
          const Text(
            'Chronological Order of Events',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 10),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: DataTable(
              columns: [
                const DataColumn(label: Text('ID')),
                const DataColumn(label: Text('Time')),
                const DataColumn(label: Text('Event Type')),
                const DataColumn(label: Text('Details')),
                if (showProbabilityColumns)
                  const DataColumn(label: Text('Arrival Probability')),
                if (showProbabilityColumns)
                  const DataColumn(label: Text('Completion Probability')),
              ],
              rows: currentData
                  .map((event) => DataRow(cells: [
                        DataCell(Text(event.customerId)),
                        DataCell(Text(event.clockTime)),
                        DataCell(Text(event.eventType)),
                        DataCell(Text(event.serviceTitle)),
                        if (showProbabilityColumns)
                          DataCell(Text(event.arrivalProb)),
                        if (showProbabilityColumns)
                          DataCell(Text(event.completionProb)),
                      ]))
                  .toList(),
            ),
          ),
        ],
      ),
    );
  }

  void generateCustomers() {
    if (services.isEmpty) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Error'),
          content: const Text(
              'No services available! Please add services first or upload an Excel file.'),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('OK'),
            ),
          ],
        ),
      );
      return;
    }

    currentData.clear();

    try {
      int customerCount = Random().nextInt(6) + 5; // Between 5 and 10 customers
      int arrivalTime = 0;

      for (int i = 1; i <= customerCount; i++) {
        int interval = Random().nextInt(3) + 1; // Between 1 and 3 minutes
        arrivalTime += interval;

        var randomServiceKey =
            services.keys.elementAt(Random().nextInt(services.length));
        var selectedService = services[randomServiceKey]!;

        String durationStr = selectedService['serviceDuration'].trim();
        int serviceDuration = int.tryParse(durationStr) ?? 0;

        int departureTime = arrivalTime + serviceDuration;

        // Add arrival event
        currentData.add(CustomerEvent(
          customerId: i.toString(),
          eventType: "Arrival",
          clockTime: arrivalTime.toString(),
          serviceCode: selectedService['serviceCode'],
          serviceTitle: selectedService['serviceTitle'],
          serviceDuration: serviceDuration.toString(),
          endTime: departureTime.toString(),
        ));

        // Add departure event
        currentData.add(CustomerEvent(
          customerId: i.toString(),
          eventType: "Departure",
          clockTime: departureTime.toString(),
          serviceCode: selectedService['serviceCode'],
          serviceTitle: selectedService['serviceTitle'],
          serviceDuration: serviceDuration.toString(),
          endTime: departureTime.toString(),
        ));
      }

      setState(() {
        updateDisplays();
      });
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Simulation Complete'),
          content: const Text('simulation process completed successfully!'),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('OK'),
            ),
          ],
        ),
      );
    } catch (e) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Error'),
          content: Text('Failed to generate customers: $e'),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('OK'),
            ),
          ],
        ),
      );
    }
  }

  void probabilitySimulation() {
    if (services.isEmpty) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Error'),
          content:
              const Text('No services available! Please add services first.'),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('OK'),
            ),
          ],
        ),
      );
      return;
    }

    try {
      double arrivalProbability = 0.6; // 60% chance of customer arrival
      double serviceCompletionProbability = 0.8;
      int maxCustomers = 20;
      List<CustomerEvent> simulatedData = [];
      int arrivalTime = 0;

      for (int customerId = 1; customerId <= maxCustomers; customerId++) {
        if (Random().nextDouble() <= arrivalProbability) {
          arrivalTime += Random().nextInt(3) + 1;

          // Select a random service
          var randomServiceKey =
              services.keys.elementAt(Random().nextInt(services.length));
          var serviceInfo = services[randomServiceKey]!;
          int serviceDuration =
              int.tryParse(serviceInfo['serviceDuration']) ?? 0;
          int departureTime = arrivalTime + serviceDuration;

          // Probability values for arrival and service completion
          double arrivalProb = Random().nextDouble();
          double completionProb = Random().nextDouble();

          // Add Arrival event
          simulatedData.add(
            CustomerEvent(
              customerId: customerId.toString(),
              eventType: 'Arrival',
              clockTime: arrivalTime.toString(),
              serviceCode: serviceInfo['serviceCode'],
              serviceTitle: serviceInfo['serviceTitle'],
              serviceDuration: serviceDuration.toString(),
              endTime: departureTime.toString(),
              arrivalProb: arrivalProb.toString(),
              completionProb: completionProb.toString(),
            ),
          );

          // Add Departure event
          simulatedData.add(
            CustomerEvent(
              customerId: customerId.toString(),
              eventType: 'Departure',
              clockTime: departureTime.toString(),
              serviceCode: serviceInfo['serviceCode'],
              serviceTitle: serviceInfo['serviceTitle'],
              serviceDuration: serviceDuration.toString(),
              endTime: departureTime.toString(),
              arrivalProb: arrivalProb.toString(),
              completionProb: completionProb.toString(),
            ),
          );
        }
      }

      if (simulatedData.isNotEmpty) {
        setState(() {
          currentData = simulatedData;
          updateDisplays();
        });

        // Show a success message
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('Probability Simulation Complete'),
            content: const Text(
                'Probability-based simulation completed successfully!'),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text('OK'),
              ),
            ],
          ),
        );
      } else {
        // No events generated
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('No Data'),
            content: const Text('No events were generated in this simulation.'),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text('OK'),
              ),
            ],
          ),
        );
      }
    } catch (e) {
      // Handle any errors that occur during the simulation
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Error'),
          content: Text('Failed to run probability simulation: $e'),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('OK'),
            ),
          ],
        ),
      );
    }
  }

  void saveAllData() async {
    if (currentData.isEmpty) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text("Warning"),
          content: const Text("No data to save!"),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text("OK"),
            ),
          ],
        ),
      );
      return;
    }

    try {
      String? filePath = await FilePicker.platform.saveFile(
        dialogTitle: 'Save Excel File',
        fileName: 'simulation_data.xlsx',
      );

      if (filePath != null) {
        var excel = Excel.createExcel();
        Sheet sheet = excel['Sheet1'];

        sheet.appendRow([
          TextCellValue('Customer ID'),
          TextCellValue('Event Type'),
          TextCellValue('Clock Time'),
          TextCellValue('Service Code'),
          TextCellValue('Service Title'),
          TextCellValue('Service Duration'),
          TextCellValue('End Time'),
        ]);

        for (var event in currentData) {
          sheet.appendRow([
            TextCellValue(event.customerId),
            TextCellValue(event.eventType),
            TextCellValue(event.clockTime),
            TextCellValue(event.serviceCode),
            TextCellValue(event.serviceTitle),
            TextCellValue(event.serviceDuration),
            TextCellValue(event.endTime),
          ]);
        }

        List<int> bytes = excel.encode() ?? [];
        File(filePath).writeAsBytesSync(bytes);

        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text("Success"),
            content: const Text("Data saved successfully!"),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text("OK"),
              ),
            ],
          ),
        );
      }
    } catch (e) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text("Error"),
          content: Text("Failed to save data: ${e.toString()}"),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text("OK"),
            ),
          ],
        ),
      );
    }
  }

  void clearAllData() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text("Confirm Clear"),
          content: const Text("Are you sure you want to clear all data?"),
          actions: [
            TextButton(
              onPressed: () {
                setState(() {
                  newData.clear();
                  currentData.clear();
                  services.clear();
                  graphDataPoints.clear();
                });
                Navigator.of(context).pop(); // Close the dialog
              },
              child: const Text("Yes"),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(); // Close the dialog
              },
              child: const Text("No"),
            ),
          ],
        );
      },
    );
  }

  void _addService() {
    final serviceCode = serviceCodeController.text;
    final serviceTitle = serviceTitleController.text;
    final serviceDuration = serviceDurationController.text;

    if (serviceCode.isNotEmpty &&
        serviceTitle.isNotEmpty &&
        serviceDuration.isNotEmpty) {
      services[serviceCode] = {
        'serviceCode': serviceCode,
        'serviceTitle': serviceTitle,
        'serviceDuration': serviceDuration,
      };
      print("Service Added: $serviceCode - $serviceTitle");

      serviceCodeController.clear();
      serviceTitleController.clear();
      serviceDurationController.clear();
    }
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
            topTitles: const AxisTitles(
              sideTitles: SideTitles(showTitles: false),
            ),
            rightTitles: const AxisTitles(
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
