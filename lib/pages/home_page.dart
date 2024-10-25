import 'dart:math';
import 'package:excel/excel.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:simulation_clock_table_main/constents.dart';
import 'package:simulation_clock_table_main/models/customer_event_model';
import 'package:simulation_clock_table_main/widgets/custom_button.dart';
import 'dart:io';
import 'package:file_picker/file_picker.dart';

class HomePage extends StatefulWidget {
  HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List<Map<String, dynamic>> newData = [];
  List<CustomerEvent> currentData = [];
  Map<String, Map<String, dynamic>> services = {};
  List<FlSpot> graphDataPoints = [];

  void initState() {
    super.initState();
  }

  final TextEditingController serviceCodeController = TextEditingController();
  final TextEditingController serviceTitleController = TextEditingController();
  final TextEditingController serviceDurationController =
      TextEditingController();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: PrimaryColor,
        title: const Text(
          'Simulation Clock Table',
          style: const TextStyle(
            color: Colors.white,
            fontSize: 25,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
          child: ListView(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Column(
                    children: [
                      CustomButton(
                          onPressed: initializeData, text: 'Upload File'),
                      const SizedBox(height: 10),
                      CustomButton(
                          onPressed: generate_customers, text: 'Simulate'),
                    ],
                  ),
                  const Divider(
                    thickness: 2,
                  ),
                  Column(
                    children: [
                      CustomButton(onPressed: saveAllData, text: 'Save Data'),
                      const SizedBox(height: 10),
                      CustomButton(onPressed: clearAllData, text: 'Clear Data'),
                    ],
                  )
                ],
              ),
              const SizedBox(height: 20),
              createServiceForm(),
              const SizedBox(height: 20),
              buildGraphDisplay(),
            ],
          ),
        ),
      ),
    );
  }

  //_________________________________________________
  // Form for adding services
  //_________________________________________________
  Widget createServiceForm() {
    return Container(
      padding: EdgeInsets.all(10),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Add New Service',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
          const SizedBox(height: 10),
          TextFormField(
            controller: serviceCodeController,
            decoration: const InputDecoration(
              labelText: 'Service Code:',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 10),
          TextFormField(
            controller: serviceTitleController,
            decoration: const InputDecoration(
              labelText: 'Service Title:',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 10),
          TextFormField(
            controller: serviceDurationController,
            decoration: const InputDecoration(
              labelText: 'Duration (min):',
              border: OutlineInputBorder(),
            ),
            keyboardType: TextInputType.number,
          ),
          const SizedBox(height: 10),
          Center(
            child: ElevatedButton(
              style: const ButtonStyle(
                fixedSize: WidgetStatePropertyAll(
                  const Size(160, 40),
                ),
                backgroundColor: MaterialStatePropertyAll(
                  PrimaryColor,
                ),
              ),
              onPressed: () {
                addService(
                  serviceCodeController.text,
                  serviceTitleController.text,
                  serviceDurationController.text,
                );
              },
              child: const Text(
                'Add Service',
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  //_________________________________________________
  // initializing Data
  //_________________________________________________
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
            print('Row: $row'); // Log the entire row
            print('Row length: ${row.length}'); // Log the row length
            if (row.isNotEmpty) {
              for (int i = 0; i < row.length; i++) {
                print(
                    'Row[$i]: ${row[i]?.value} (type: ${row[i]?.value.runtimeType})');
              }
              var customerId = row.length > 0 ? row[0]?.value : null;
              var eventType = row.length > 1 ? row[1]?.value : null;
              var clockTime = row.length > 2 ? row[2]?.value : null;
              var serviceCode = row.length > 3 ? row[3]?.value : null;
              var serviceTitle = row.length > 4 ? row[4]?.value : null;
              var serviceDuration = row.length > 5 ? row[5]?.value : null;
              var endTime = row.length > 6 ? row[6]?.value : null;
              print(
                  'Customer ID: $customerId, Event Type: $eventType, Clock Time: $clockTime');
              currentData.add(CustomerEvent(
                customerId: customerId?.toString() ?? '',
                eventType: eventType?.toString() ?? '',
                clockTime: clockTime?.toString() ?? '',
                serviceCode: serviceCode?.toString() ?? '',
                serviceTitle: serviceTitle?.toString() ?? '',
                serviceDuration: serviceDuration?.toString() ?? '',
                endTime: endTime?.toString() ?? '',
              ));
            }
          }
        }
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

  //_________________________________________________
// build Data Table
//_________________________________________________
  Widget buildCustomerDataTable() {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: DataTable(
        columns: const [
          DataColumn(label: Text('Customer ID')),
          DataColumn(label: Text('Event Type')),
          DataColumn(label: Text('Clock Time')),
          DataColumn(label: Text('Service Code')),
          DataColumn(label: Text('Service Title')),
          DataColumn(label: Text('Service Duration')),
          DataColumn(label: Text('End Time')),
        ],
        rows: newData.map((data) {
          return DataRow(cells: [
            DataCell(Text(data['Customer ID'].toString())),
            DataCell(Text(data['Event Type'].toString())),
            DataCell(Text(data['Clock Time'].toString())),
            DataCell(Text(data['Service Code'].toString())),
            DataCell(Text(data['Service Title'].toString())),
            DataCell(Text(data['Service Duration'].toString())),
            DataCell(Text(data['End Time'].toString())),
          ]);
        }).toList(),
      ),
    );
  }

//________________________________________________
// generate Chronological Data
//________________________________________________
  void generateChronologicalData() {
    newData = [
      {
        'Time': '08:00',
        'Event Type': 'Arrival',
        'Customer ID': '1',
        'Service': 'Check-in'
      },
      {
        'Time': '08:15',
        'Event Type': 'Departure',
        'Customer ID': '1',
        'Service': 'Check-out'
      },
    ];
    setState(() {
      updateChronologicalTable();
    });
  }

  Widget buildChronologicalEventsTable() {
    return Padding(
      padding: const EdgeInsets.all(10.0),
      child: Column(
        children: [
          Text(
            'Chronological Order of Events',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 10),
          Expanded(
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: DataTable(
                columns: const [
                  DataColumn(label: Text('Time')),
                  DataColumn(label: Text('Event Type')),
                  DataColumn(label: Text('Customer ID')),
                  DataColumn(label: Text('Service')),
                ],
                rows: newData.map((data) {
                  return DataRow(cells: [
                    DataCell(Text(data['Time'].toString())),
                    DataCell(Text(data['Event Type'].toString())),
                    DataCell(Text(data['Customer ID'].toString())),
                    DataCell(Text(data['Service'].toString())),
                  ]);
                }).toList(),
              ),
            ),
          ),
        ],
      ),
    );
  }

//_____________________________________________
// build Graph
//____________________________________________
  Widget buildGraphDisplay() {
    return Container(
      padding: const EdgeInsets.all(10.0),
      height: 300,
      child: LineChart(
        LineChartData(
          gridData: FlGridData(show: true),
          titlesData: FlTitlesData(
            leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: true)),
            bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true)),
          ),
          borderData: FlBorderData(show: true),
          lineBarsData: [
            LineChartBarData(
              spots: graphDataPoints,
              isCurved: true,
              barWidth: 3,
              color: Colors.blue,
              belowBarData: BarAreaData(show: false),
              dotData: FlDotData(show: false),
            ),
          ],
        ),
      ),
    );
  }

  List<FlSpot> _generateDataPoints() {
    List<FlSpot> dataPoints = [];
    for (int i = 0; i < newData.length; i++) {
      var event = newData[i];
      double time = double.parse(event['Time'].toString().replaceAll(':', '.'));
      dataPoints.add(FlSpot(time, i.toDouble()));
    }
    return dataPoints;
  }

//_________________________________________________
  // Add Service logic
  //_________________________________________________
  void addService(String code, String title, String durationStr) {
    try {
      code = code.trim();
      title = title.trim();
      durationStr = durationStr.trim();
      if (code.isEmpty || title.isEmpty || durationStr.isEmpty) {
        throw Exception("Please fill all fields.");
      }
      int duration = int.parse(durationStr);
      if (duration <= 0) {
        throw Exception("Duration must be a positive number.");
      }
      if (services.containsKey(code)) {
        throw Exception("Service code '$code' already exists.");
      }
      services[code] = {'title': title, 'duration': duration};
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text("Success"),
            content: Text("Service $title added successfully!"),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: const Text("OK"),
              ),
            ],
          );
        },
      );
    } catch (e) {
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text("Error"),
            content: Text(e.toString()),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: const Text("OK"),
              ),
            ],
          );
        },
      );
    }
  }

//_________________________________________________
//Simulation proccess
//_________________________________________________
  void generate_customers() {
    newData.clear();
    if (currentData.isEmpty) {
      print('No services available! Please add services first.');
      return;
    }
    try {
      final Random random = Random();
      final int numCustomers =
          random.nextInt(6) + 5; // Random number between 5 and 10
      int arrivalTime = 0;
      for (int customerId = 1; customerId <= numCustomers; customerId++) {
        int interval = random.nextInt(3) + 1; // Random interval between 1 and 3
        arrivalTime += interval;
        String serviceCode =
            services.keys.elementAt(random.nextInt(services.length));
        var serviceInfo = services[serviceCode];
        int serviceDuration = serviceInfo!['duration'];
        int departureTime = arrivalTime + serviceDuration;
        for (var eventType in ['Arrival', 'Departure']) {
          int clockTime = eventType == 'Arrival' ? arrivalTime : departureTime;
          newData.add({
            'Customer ID': customerId.toString(),
            'Event Type': eventType,
            'Clock Time': clockTime.toString(),
            'Service Code': serviceCode,
            'Service Title': serviceInfo['title'].toString(),
            'Service Duration': serviceDuration.toString(),
            'End Time': departureTime.toString(),
          });
        }
      }
      updateDisplays();
    } catch (e) {
      print('Failed to generate customers: $e');
    }
  }

  void updateDisplays() {
    updateCustomerDataTable();
    updateChronologicalTable();
    updateGraphData();
  }

//________________________________________________
// Update Customer Data Table
//_________________________________________________
  void updateCustomerDataTable() {
    currentData.sort((a, b) => a.clockTime.compareTo(b.clockTime));
    newData = currentData.map((customerEvent) {
      return {
        'Customer ID': customerEvent.customerId,
        'Event Type': customerEvent.eventType,
        'Clock Time': customerEvent.clockTime,
        'Service Code': customerEvent.serviceCode,
        'Service Title': customerEvent.serviceTitle,
        'Service Duration': customerEvent.serviceDuration,
        'End Time': customerEvent.endTime,
      };
    }).toList();
    setState(() {});
  }

//________________________________________________
// Update Chronological Table
//________________________________________________
  void updateChronologicalTable() {
    newData.clear();
    currentData.sort((a, b) => a.clockTime.compareTo(b.clockTime));
    for (var customerEvent in currentData) {
      newData.add({
        'Time': customerEvent.clockTime.toString(), // Ensure this is a String
        'Event Type':
            customerEvent.eventType.toString(), // Ensure this is a String
        'Customer ID':
            customerEvent.customerId.toString(), // Ensure this is a String
        'Service':
            customerEvent.serviceTitle.toString(), // Ensure this is a String
      });
    }
    setState(() {});
  }

//_____________________________________________________
// Update Graph Data
//____________________________________________________
  void updateGraphData() {
    if (currentData.isNotEmpty) {
      try {
        currentData.sort((a, b) => a.clockTime.compareTo(b.clockTime));
        int customerCount = 0;
        graphDataPoints.clear();
        for (var event in currentData) {
          if (event.eventType == 'Arrival') {
            customerCount++;
          } else if (event.eventType == 'Departure') {
            customerCount--;
          }
          double clockTime = double.parse(event.clockTime.replaceAll(':', '.'));
          graphDataPoints.add(FlSpot(clockTime, customerCount.toDouble()));
        }
        setState(() {});
      } catch (e) {
        print('Failed to update graph data: $e');
      }
    } else {
      graphDataPoints.clear();
      setState(() {});
    }
  }

//_______________________________________________________
// Add Graph Annotations
//_______________________________________________________
  void _addGraphAnnotations() {
    if (newData.isNotEmpty) {
      double yOffset = 0;
      int prevY = 0;
      for (var row in newData) {
        double currentY = row['Customers in System'];
        if ((currentY - prevY).abs() < 0.1) {
          yOffset = (yOffset + 0.2) % 0.6;
        } else {
          yOffset = 0;
        }
        prevY = currentY.toInt();
      }
    } else {
      _showEmptyGraph();
    }
  }

  void _showEmptyGraph() {
    // This method would set a state to show a message or a placeholder
    print('No data to display');
  }

//_______________________________________________________
// Save All Data
//_______________________________________________________
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
        var excel = Excel.createExcel(); // Create a new Excel document
        Sheet sheet = excel['Sheet1'];
        sheet.appendRow([
          'Customer ID',
          'Event Type',
          'Clock Time',
          'Service Code',
          'Service Title',
          'Service Duration',
          'End Time'
        ]);
        for (var event in currentData) {
          sheet.appendRow([
            event.customerId,
            event.eventType,
            event.clockTime,
            event.serviceCode,
            event.serviceTitle,
            event.serviceDuration,
            event.endTime,
          ]);
        }
        List<int> bytes = excel.encode() ?? []; // Handle nullable return
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

//_______________________________________________________
// Clear All Data
//_______________________________________________________
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
}