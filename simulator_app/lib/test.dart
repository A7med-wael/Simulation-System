// void probabilitySimulation() {
  //   if (services.isEmpty) {
  //     showDialog(
  //       context: context,
  //       builder: (context) => AlertDialog(
  //         title: const Text('Error'),
  //         content:
  //             const Text('No services available! Please add services first.'),
  //         actions: [
  //           TextButton(
  //             onPressed: () => Navigator.of(context).pop(),
  //             child: const Text('OK'),
  //           ),
  //         ],
  //       ),
  //     );
  //     return;
  //   }

  //   try {
  //     double arrivalProbability =
  //         0.6; // 60% chance of customer arrival per time unit
  //     double serviceCompletionProbability = 0.8;
  //     int maxCustomers = 20;
  //     List<CustomerEvent> simulatedData = [];
  //     // List<Map<String, dynamic>> simulatedData = [];
  //     int arrivalTime = 0;

  //     for (int customerId = 1; customerId <= maxCustomers; customerId++) {
  //       if (Random().nextDouble() <= arrivalProbability) {
  //         arrivalTime += Random().nextInt(3) +
  //             1; // Random interval between 1 and 3 minutes

  //         var randomServiceKey =
  //             services.keys.elementAt(Random().nextInt(services.length));
  //         var serviceInfo = services[randomServiceKey]!;
  //         int serviceDuration =
  //             int.tryParse(serviceInfo['serviceDuration']) ?? 0;
  //         int departureTime = arrivalTime + serviceDuration;

  //         // Probability-based columns
  //         double arrivalProb = Random().nextDouble();
  //         double completionProb = serviceCompletionProbability;

  //         simulatedData.add(
  //           CustomerEvent(
  //             customerId: customerId.toString(),
  //             eventType: 'Arrival',
  //             clockTime: arrivalTime.toString(),
  //             serviceCode: serviceInfo['serviceCode'],
  //             serviceTitle: serviceInfo['serviceTitle'],
  //             serviceDuration: serviceDuration.toString(),
  //             endTime: departureTime.toString(),
  //             arrivalProb: arrivalProb.toString(),
  //             completionProb: completionProb.toString(),
  //           ),
  //         );
  //         simulatedData.add(
  //           CustomerEvent(
  //             customerId: customerId.toString(),
  //             eventType: 'Departure',
  //             clockTime: departureTime.toString(),
  //             serviceCode: serviceInfo['serviceCode'],
  //             serviceTitle: serviceInfo['serviceTitle'],
  //             serviceDuration: serviceDuration.toString(),
  //             endTime: departureTime.toString(),
  //             arrivalProb: arrivalProb.toString(),
  //             completionProb: completionProb.toString(),
  //           ),
  //         );
  //       }

  //       // currentData = simulatedData.cast<CustomerEvent>();

  //       setState(() {
  //         currentData = simulatedData;
  //         updateDisplays();
  //       });

  //       showDialog(
  //         context: context,
  //         builder: (context) => AlertDialog(
  //           title: const Text('Probability Simulation Complete'),
  //           content: const Text(
  //               'Probability-based simulation completed successfully!'),
  //           actions: [
  //             TextButton(
  //               onPressed: () => Navigator.of(context).pop(),
  //               child: const Text('OK'),
  //             ),
  //           ],
  //         ),
  //       );
  //     }
  //   } catch (e) {
  //     showDialog(
  //       context: context,
  //       builder: (context) => AlertDialog(
  //         title: const Text('Error'),
  //         content: Text('Failed to run probability simulation: $e'),
  //         actions: [
  //           TextButton(
  //             onPressed: () => Navigator.of(context).pop(),
  //             child: const Text('OK'),
  //           ),
  //         ],
  //       ),
  //     );
  //   }
  // }


// import 'dart:math';
// import 'dart:io';
// import 'package:excel/excel.dart';
// import 'package:fl_chart/fl_chart.dart';
// import 'package:flutter/material.dart';
// import 'package:file_picker/file_picker.dart';

// class HomePage extends StatefulWidget {
//   const HomePage({super.key});

//   @override
//   State<HomePage> createState() => _HomePageState();
// }

// class _HomePageState extends State<HomePage> {
//   final TextEditingController serviceCodeController = TextEditingController();
//   final TextEditingController serviceTitleController = TextEditingController();
//   final TextEditingController serviceDurationController =
//       TextEditingController();

//   List<Map<String, dynamic>> newData = [];
//   List<CustomerEvent> currentData = [];
//   List<Map<String, dynamic>> customerData = [];
//   Map<String, Map<String, dynamic>> services = {};
//   List<FlSpot> graphDataPoints = [];

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: _buildAppBar(),
//       body: Center(
//         child: Padding(
//           padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
//           child: ListView(
//             children: [
//               _buildActionButtons(),
//               const SizedBox(height: 20),
//               _buildServiceForm(),
//               const SizedBox(height: 20),
//               buildGraphDisplay(),
//               const SizedBox(height: 20),
//               buildCustomerDataTable(),
//               const SizedBox(height: 20),
//               buildChronologicalEventsTable(),
//             ],
//           ),
//         ),
//       ),
//     );
//   }

//   AppBar _buildAppBar() {
//     return AppBar(
//       backgroundColor:
//           Colors.blue, // Replace `PrimaryColor` with a color directly
//       title: const Text(
//         'Simulation Clock Table',
//         style: TextStyle(
//           color: Colors.white,
//           fontSize: 25,
//           fontWeight: FontWeight.bold,
//         ),
//       ),
//     );
//   }

//   // Action buttons for uploading file, simulating data, saving, and clearing data
//   Widget _buildActionButtons() {
//     return Row(
//       mainAxisAlignment: MainAxisAlignment.spaceAround,
//       children: [
//         _buildColumnButtons([
//           CustomButton(onPressed: initializeData, text: 'Upload File'),
//           CustomButton(onPressed: generateCustomers, text: 'Simulate'),
//         ]),
//         const Divider(thickness: 2),
//         _buildColumnButtons([
//           CustomButton(onPressed: saveAllData, text: 'Save Data'),
//           CustomButton(onPressed: clearAllData, text: 'Clear Data'),
//         ]),
//       ],
//     );
//   }

//   Widget _buildColumnButtons(List<Widget> buttons) {
//     return Column(
//       children: buttons
//           .map((button) => Padding(
//                 padding: const EdgeInsets.symmetric(vertical: 5),
//                 child: button,
//               ))
//           .toList(),
//     );
//   }

//   Widget _buildServiceForm() {
//     return Container(
//       padding: const EdgeInsets.all(10),
//       decoration: BoxDecoration(
//         borderRadius: BorderRadius.circular(10),
//       ),
//       child: Column(
//         crossAxisAlignment: CrossAxisAlignment.start,
//         children: [
//           const Text('Add New Service',
//               style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
//           const SizedBox(height: 10),
//           _buildTextInputField(
//               controller: serviceCodeController, labelText: 'Service Code:'),
//           _buildTextInputField(
//               controller: serviceTitleController, labelText: 'Service Title:'),
//           _buildTextInputField(
//               controller: serviceDurationController,
//               labelText: 'Duration (min):',
//               keyboardType: TextInputType.number),
//           const SizedBox(height: 10),
//           _buildAddServiceButton(),
//         ],
//       ),
//     );
//   }

//   Widget _buildTextInputField({
//     required TextEditingController controller,
//     required String labelText,
//     TextInputType keyboardType = TextInputType.text,
//   }) {
//     return Padding(
//       padding: const EdgeInsets.only(bottom: 10),
//       child: TextFormField(
//         controller: controller,
//         decoration: InputDecoration(
//           labelText: labelText,
//           border: const OutlineInputBorder(),
//         ),
//         keyboardType: keyboardType,
//       ),
//     );
//   }

//   Widget _buildAddServiceButton() {
//     return Center(
//       child: ElevatedButton(
//         style: ButtonStyle(
//           fixedSize: WidgetStateProperty.all(const Size(160, 40)),
//           backgroundColor: WidgetStateProperty.all(
//               Colors.blue), // Replace `PrimaryColor` here
//         ),
//         onPressed: _addService,
//         child: const Text(
//           'Add Service',
//           style: TextStyle(
//             color: Colors.white,
//             fontSize: 20,
//             fontWeight: FontWeight.bold,
//           ),
//         ),
//       ),
//     );
//   }

//   Future<void> initializeData() async {
//     FilePickerResult? result = await FilePicker.platform.pickFiles(
//       type: FileType.custom,
//       allowedExtensions: ['xlsx', 'xls'],
//     );

//     if (result != null && result.files.isNotEmpty) {
//       String? filePath = result.files.single.path;
//       var file = File(filePath!);
//       try {
//         var bytes = file.readAsBytesSync();
//         var excel = Excel.decodeBytes(bytes);
//         for (var table in excel.tables.keys) {
//           for (var row in excel.tables[table]!.rows) {
//             if (row.isNotEmpty) {
//               // Extract the service details based on the image
//               var serviceCode = row[0]?.value; // Column 1: Service Code
//               var serviceTitle = row[1]?.value; // Column 2: Service Title
//               var serviceDuration =
//                   row[2]?.value; // Column 3: Service Duration (minutes)

//               // Check for valid services and add to the services map
//               if (serviceCode != null &&
//                   serviceTitle != null &&
//                   serviceDuration != null) {
//                 services[serviceCode.toString()] = {
//                   'serviceCode': serviceCode.toString(),
//                   'serviceTitle': serviceTitle.toString(),
//                   'serviceDuration': serviceDuration.toString(),
//                 };
//               }
//             }
//           }
//         }

//         print("Services Loaded: $services");
//         setState(() {
//           updateDisplays();
//         });
//       } catch (e) {
//         print('Error while processing Excel file: $e');
//       }
//     } else {
//       print('No file selected');
//     }
//   }

//   void _processExcelFile(String filePath) {
//     try {
//       final bytes = File(filePath).readAsBytesSync();
//       final excel = Excel.decodeBytes(bytes);
//       currentData = _extractExcelData(excel);
//       setState(() {
//         updateDisplays();
//       });
//     } catch (e) {
//       print('Error while processing Excel file: $e');
//     }
//   }

//   void updateDisplays() {
//     // Update the graph data points based on currentData
//     graphDataPoints = List.generate(currentData.length, (index) {
//       // Ensure serviceDuration is parsed as a double
//       double serviceDuration =
//           double.tryParse(currentData[index].serviceDuration) ?? 0.0;

//       return FlSpot(index.toDouble(), serviceDuration);
//     });

//     // Update newData with the currentData for the DataTables to display
//     newData = currentData.map((event) {
//       return {
//         'Customer ID': event.customerId,
//         'Event Type': event.eventType,
//         'Clock Time': event.clockTime,
//         'Service Code': event.serviceCode,
//         'Service Title': event.serviceTitle,
//         'Service Duration': event.serviceDuration,
//         'End Time': event.endTime,
//       };
//     }).toList();

//     setState(() {}); // Refresh the UI with the updated data
//   }

//   List<CustomerEvent> _extractExcelData(Excel excel) {
//     final List<CustomerEvent> data = [];
//     for (var table in excel.tables.keys) {
//       for (var row in excel.tables[table]!.rows) {
//         if (row.isNotEmpty) {
//           data.add(CustomerEvent(
//             customerId: row[0]?.value.toString() ?? '',
//             eventType: row[1]?.value.toString() ?? '',
//             clockTime: row[2]?.value.toString() ?? '',
//             serviceCode: row[3]?.value.toString() ?? '',
//             serviceTitle: row[4]?.value.toString() ?? '',
//             serviceDuration: row[5]?.value.toString() ?? '',
//             endTime: row[6]?.value.toString() ?? '',
//           ));
//         }
//       }
//     }
//     return data;
//   }

  // Widget buildCustomerDataTable() {
  //   return SingleChildScrollView(
  //     scrollDirection: Axis.horizontal,
  //     child: DataTable(
  //       columns: const [
  //         DataColumn(label: Text('Customer ID')),
  //         DataColumn(label: Text('Event Type')),
  //         DataColumn(label: Text('Clock Time')),
  //         DataColumn(label: Text('Service Code')),
  //         DataColumn(label: Text('Service Title')),
  //         DataColumn(label: Text('Service Duration')),
  //         DataColumn(label: Text('End Time')),
  //       ],
  //       rows: newData.map((data) => _buildDataRow(data)).toList(),
  //     ),
  //   );
  // }

  // DataRow _buildDataRow(Map<String, dynamic> data) {
  //   return DataRow(cells: [
  //     DataCell(Text(data['Customer ID'].toString())),
  //     DataCell(Text(data['Event Type'].toString())),
  //     DataCell(Text(data['Clock Time'].toString())),
  //     DataCell(Text(data['Service Code'].toString())),
  //     DataCell(Text(data['Service Title'].toString())),
  //     DataCell(Text(data['Service Duration'].toString())),
  //     DataCell(Text(data['End Time'].toString())),
  //   ]);
  // }

  // Widget buildChronologicalEventsTable() {
  //   return Padding(
  //     padding: const EdgeInsets.all(10.0),
  //     child: Column(
  //       children: [
  //         const Text(
  //           'Chronological Order of Events',
  //           style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
  //         ),
  //         const SizedBox(height: 10),
  //         SingleChildScrollView(
  //           scrollDirection: Axis.horizontal,
  //           child: DataTable(
  //             columns: const [
  //               DataColumn(label: Text('Time')),
  //               DataColumn(label: Text('Event Type')),
  //               DataColumn(label: Text('Details')),
  //             ],
  //             rows: currentData
  //                 .map((event) => DataRow(cells: [
  //                       DataCell(Text(event.clockTime)),
  //                       DataCell(Text(event.eventType)),
  //                       DataCell(Text(event.serviceTitle)),
  //                     ]))
  //                 .toList(),
  //           ),
  //         ),
  //       ],
  //     ),
  //   );
  // }

//   void generateCustomers() {
//   if (services.isEmpty) {
//     showDialog(
//       context: context,
//       builder: (context) => AlertDialog(
//         title: const Text('Error'),
//         content: const Text(
//             'No services available! Please add services first or upload an Excel file.'),
//         actions: [
//           TextButton(
//             onPressed: () => Navigator.of(context).pop(),
//             child: const Text('OK'),
//           ),
//         ],
//       ),
//     );
//     return;
//   }

//   // Clear the previous customer data
//   currentData.clear();

//   try {
//     int customerCount = Random().nextInt(6) + 5; // Between 5 and 10 customers
//     int arrivalTime = 0;

//     // Simulate customers
//     for (int i = 1; i <= customerCount; i++) {
//       int interval = Random().nextInt(3) + 1; // Between 1 and 3 minutes
//       arrivalTime += interval;

//       // Randomly select a service from the loaded services
//       var randomServiceKey = services.keys.elementAt(Random().nextInt(services.length));
//       var selectedService = services[randomServiceKey]!;

//       // Ensure the service duration is a valid integer
//       String durationStr = selectedService['serviceDuration'].trim();
//       int serviceDuration = int.tryParse(durationStr) ?? 0;

//       int departureTime = arrivalTime + serviceDuration;

//       // Add arrival event
//       currentData.add(CustomerEvent(
//         customerId: i.toString(),
//         eventType: "Arrival",
//         clockTime: arrivalTime.toString(),
//         serviceCode: selectedService['serviceCode'],
//         serviceTitle: selectedService['serviceTitle'],
//         serviceDuration: serviceDuration.toString(),
//         endTime: departureTime.toString(),
//       ));

//       // Add departure event
//       currentData.add(CustomerEvent(
//         customerId: i.toString(),
//         eventType: "Departure",
//         clockTime: departureTime.toString(),
//         serviceCode: selectedService['serviceCode'],
//         serviceTitle: selectedService['serviceTitle'],
//         serviceDuration: serviceDuration.toString(),
//         endTime: departureTime.toString(),
//       ));
//     }

//     // Update the display
//     setState(() {
//       updateDisplays(); // Refresh the UI with the new data
//     });
//   } catch (e) {
//     showDialog(
//       context: context,
//       builder: (context) => AlertDialog(
//         title: const Text('Error'),
//         content: Text('Failed to generate customers: $e'),
//         actions: [
//           TextButton(
//             onPressed: () => Navigator.of(context).pop(),
//             child: const Text('OK'),
//           ),
//         ],
//       ),
//     );
//   }
// }
//   void saveAllData() {
//     print("Saving all data...");
//     // Code for saving all data
//   }

//   void clearAllData() {
//         showDialog(
//       context: context,
//       builder: (BuildContext context) {
//         return AlertDialog(
//           title: const Text("Confirm Clear"),
//           content: const Text("Are you sure you want to clear all data?"),
//           actions: [
//             TextButton(
//               onPressed: () {
//                 setState(() {
//                   newData.clear();
//                   currentData.clear();
//                   services.clear();
//                   graphDataPoints.clear();
//                 });
//                 Navigator.of(context).pop(); // Close the dialog
//               },
//               child: const Text("Yes"),
//             ),
//             TextButton(
//               onPressed: () {
//                 Navigator.of(context).pop(); // Close the dialog
//               },
//               child: const Text("No"),
//             ),
//           ],
//         );
//       },
//     );
//   }

//   // Adds a new service to the services map
//   void _addService() {
//     final serviceCode = serviceCodeController.text;
//     final serviceTitle = serviceTitleController.text;
//     final serviceDuration = serviceDurationController.text;

//     if (serviceCode.isNotEmpty &&
//         serviceTitle.isNotEmpty &&
//         serviceDuration.isNotEmpty) {
//       services[serviceCode] = {
//         'serviceCode': serviceCode,
//         'serviceTitle': serviceTitle,
//         'serviceDuration': serviceDuration,
//       };
//       print("Service Added: $serviceCode - $serviceTitle");

//       serviceCodeController.clear();
//       serviceTitleController.clear();
//       serviceDurationController.clear();
//     }
//   }

//   // Displays the graph using the FlChart library
//   Widget buildGraphDisplay() {
//     return Container(
//       height: 200,
//       width: double.infinity,
//       decoration: BoxDecoration(
//         borderRadius: BorderRadius.circular(10),
//       ),
//       child: LineChart(
//         LineChartData(
//           lineBarsData: [
//             LineChartBarData(
//               spots: graphDataPoints,
//               isCurved: true,
//               color: Colors.blue, // Replace PrimaryColor here
//               belowBarData: BarAreaData(show: false),
//             ),
//           ],
//           gridData: FlGridData(show: true),
//           titlesData: FlTitlesData(show: true),
//         ),
//       ),
//     );
//   }
// }

// class CustomerEvent {
//   final String customerId;
//   final String eventType;
//   final String clockTime;
//   final String serviceCode;
//   final String serviceTitle;
//   final String serviceDuration;
//   final String endTime;

//   CustomerEvent({
//     required this.customerId,
//     required this.eventType,
//     required this.clockTime,
//     required this.serviceCode,
//     required this.serviceTitle,
//     required this.serviceDuration,
//     required this.endTime,
//   });
// }

// class CustomButton extends StatelessWidget {
//   final VoidCallback onPressed;
//   final String text;

//   const CustomButton({
//     super.key,
//     required this.onPressed,
//     required this.text,
//   });

//   @override
//   Widget build(BuildContext context) {
//     return ElevatedButton(
//       style: const ButtonStyle(
//           backgroundColor: WidgetStatePropertyAll(Colors.blue)),
//       onPressed: onPressed,
//       child: Text(
//         text,
//         style: const TextStyle(color: Colors.white, fontSize: 16),
//       ),
//     );
//   }
// }