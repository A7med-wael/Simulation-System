 // Widget _buildActionButtons() {
  //   return Column(
  //     children: [
  //       CustomButton(onPressed: initializeData, text: 'Upload File'),
  // CustomButton(
  //     onPressed: () {
  //       setState(() {
  //         showProbabilityColumns = false;
  //         generateCustomers(
  //         services: services,
  //         currentData: currentData,
  //         context: context,
  //         updateDisplays: updateDisplays,
  //       );
  //       });
  //     },
  //     text: 'Simulate'),
  // CustomButton(
  //     onPressed: () {
  //       setState(() {
  //         showProbabilityColumns = true;
  //         probabilitySimulation();
  //       });
  //     },
  //     text: 'Probability'),
  //     ],
  //   );
  // }

  // Widget _buildServiceForm() {
  //   return Container(
  //     padding: const EdgeInsets.all(10),
  //     decoration: BoxDecoration(
  //       borderRadius: BorderRadius.circular(10),
  //     ),
  //     child: Column(
  //       crossAxisAlignment: CrossAxisAlignment.start,
  //       children: [
  //         const Center(
  //           child:  Text('Add New Service',
  //               style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
  //         ),
  //         const SizedBox(height: 10),
  //         _buildTextInputField(
  //             controller: serviceCodeController, labelText: 'Service Code:'),
  //         _buildTextInputField(
  //             controller: serviceTitleController, labelText: 'Service Title:'),
  //         _buildTextInputField(
  //             controller: serviceDurationController,
  //             labelText: 'Duration (min):',
  //             keyboardType: TextInputType.number),
  //         const SizedBox(height: 10),
  //         Center(
  //           child: CustomButton(
  //             onPressed: _addService,
  //             text: 'Add Service',
  //           ),
  //         ),
  //       ],
  //     ),
  //   );
  // }

  // Widget _buildTextInputField({
  //   required TextEditingController controller,
  //   required String labelText,
  //   TextInputType keyboardType = TextInputType.text,
  // }) {
  //   return Padding(
  //     padding: const EdgeInsets.only(bottom: 10),
  //     child: TextFormField(
  //       controller: controller,
  //       decoration: InputDecoration(
  //         labelText: labelText,
  //         border: const OutlineInputBorder(),
  //       ),
  //       keyboardType: keyboardType,
  //     ),
  //   );
  // }

  // Future<void> initializeData() async {
  //   FilePickerResult? result = await FilePicker.platform.pickFiles(
  //     type: FileType.custom,
  //     allowedExtensions: ['xlsx', 'xls'],
  //   );
  //   if (result != null && result.files.isNotEmpty) {
  //     String? filePath = result.files.single.path;
  //     var file = File(filePath!);
  //     try {
  //       var bytes = file.readAsBytesSync();
  //       var excel = Excel.decodeBytes(bytes);
  //       for (var table in excel.tables.keys) {
  //         for (var row in excel.tables[table]!.rows) {
  //           if (row.isNotEmpty) {
  //             var serviceCode = row[0]?.value;
  //             var serviceTitle = row[1]?.value;
  //             var serviceDuration = row[2]?.value;
  //             if (serviceCode != null &&
  //                 serviceTitle != null &&
  //                 serviceDuration != null) {
  //               services[serviceCode.toString()] = {
  //                 'serviceCode': serviceCode.toString(),
  //                 'serviceTitle': serviceTitle.toString(),
  //                 'serviceDuration': serviceDuration.toString(),
  //               };
  //             }
  //           }
  //         }
  //       }
  //       showDialog(
  //         context: context,
  //         builder: (context) => AlertDialog(
  //           title: const Text('File Loaded'),
  //           content: const Text('File loaded successfully.'),
  //           actions: [
  //             TextButton(
  //               onPressed: () => Navigator.of(context).pop(),
  //               child: const Text('OK'),
  //             ),
  //           ],
  //         ),
  //       );
  //       print("Services Loaded: $services");
  //       setState(() {
  //         updateDisplays();
  //       });
  //     } catch (e) {
  //       print('Error while processing Excel file: $e');
  //     }
  //   } else {
  //     print('No file selected');
  //   }
  // }

  // Widget buildCustomerDataTable() {
  //   return Column(
  //     children: [
  //       const Text(
  //         'Customer Data Table',
  //         style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
  //       ),
  //       SingleChildScrollView(
  //         scrollDirection: Axis.horizontal,
  //         child: DataTable(
  //           columns: [
  //             const DataColumn(label: Text('Customer ID')),
  //             const DataColumn(label: Text('Event Type')),
  //             const DataColumn(label: Text('Clock Time')),
  //             const DataColumn(label: Text('Service Code')),
  //             const DataColumn(label: Text('Service Title')),
  //             const DataColumn(label: Text('Service Duration')),
  //             const DataColumn(label: Text('End Time')),
  //             if (showProbabilityColumns)
  //               const DataColumn(label: Text('Arrival Probability')),
  //             if (showProbabilityColumns)
  //               const DataColumn(label: Text('Completion Probability')),
  //           ],
  //           rows: newData.map((data) => _buildDataRow(data)).toList(),
  //         ),
  //       ),
  //     ],
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
  //     if (showProbabilityColumns)
  //       DataCell(Text(data['Arrival Probability'].toString())),
  //     if (showProbabilityColumns)
  //       DataCell(Text(data['Completion Probability'].toString())),
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
  //         SingleChildScrollView(
  //           scrollDirection: Axis.horizontal,
  //           child: DataTable(
  //             columns: [
  //               const DataColumn(label: Text('ID')),
  //               const DataColumn(label: Text('Time')),
  //               const DataColumn(label: Text('Event Type')),
  //               const DataColumn(label: Text('Details')),
  //               if (showProbabilityColumns)
  //                 const DataColumn(label: Text('Arrival Probability')),
  //               if (showProbabilityColumns)
  //                 const DataColumn(label: Text('Completion Probability')),
  //             ],
  //             rows: currentData
  //                 .map((event) => DataRow(cells: [
  //                       DataCell(Text(event.customerId)),
  //                       DataCell(Text(event.clockTime)),
  //                       DataCell(Text(event.eventType)),
  //                       DataCell(Text(event.serviceTitle)),
  //                       if (showProbabilityColumns)
  //                         DataCell(Text(event.arrivalProb)),
  //                       if (showProbabilityColumns)
  //                         DataCell(Text(event.completionProb)),
  //                     ]))
  //                 .toList(),
  //           ),
  //         ),
  //       ],
  //     ),
  //   );
  // }
 
 // void generateCustomers() {
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
  //   List<CustomerEvent> tempEvents = [];
  //   Map<String, dynamic> endtime = {};
  //   try {
  //     int customerCount = Random().nextInt(6) + 5;
  //     int arrivalTime = 0;
  //     for (int i = 1; i <= customerCount; i++) {
  //       int interval = Random().nextInt(3) + 0;
  //       arrivalTime += interval;
  //       var randomServiceKey =
  //           services.keys.elementAt(Random().nextInt(services.length));
  //       var selectedService = services[randomServiceKey]!;
  //       // int serviceDuration = int.parse(selectedService['serviceDuration']);
  //       String durationStr = selectedService['serviceDuration'].trim();
  //       int serviceDuration = int.tryParse(durationStr) ?? 0;
  //       if (endtime.containsKey(randomServiceKey)) {
  //         arrivalTime = max(endtime[randomServiceKey]!, arrivalTime);
  //       } else {
  //         arrivalTime = arrivalTime;
  //       }
  //       int departureTime = arrivalTime + serviceDuration;
  //       endtime[randomServiceKey] = departureTime;
  //       tempEvents.add(CustomerEvent(
  //         customerId: i.toString(),
  //         eventType: "Arrival",
  //         clockTime: arrivalTime.toString(),
  //         serviceCode: selectedService['serviceCode'],
  //         serviceTitle: selectedService['serviceTitle'],
  //         serviceDuration: serviceDuration.toString(),
  //         endTime: departureTime.toString(),
  //       ));
  //       tempEvents.add(CustomerEvent(
  //         customerId: i.toString(),
  //         eventType: "Departure",
  //         clockTime: departureTime.toString(),
  //         serviceCode: selectedService['serviceCode'],
  //         serviceTitle: selectedService['serviceTitle'],
  //         serviceDuration: serviceDuration.toString(),
  //         endTime: departureTime.toString(),
  //       ));
  //     }
  //     tempEvents.sort((a, b) {
  //       return int.parse(a.clockTime).compareTo(int.parse(b.clockTime));
  //     });
  //     currentData.clear();
  //     currentData.addAll(tempEvents);
  //     setState(() {
  //       updateDisplays();
  //     });
  //     showDialog(
  //       context: context,
  //       builder: (context) => AlertDialog(
  //         title: const Text('Simulation Complete'),
  //         content: const Text('Simulation process completed successfully!'),
  //         actions: [
  //           TextButton(
  //             onPressed: () => Navigator.of(context).pop(),
  //             child: const Text('OK'),
  //           ),
  //         ],
  //       ),
  //     );
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

//   void generateCustomersWithTwoServers() {
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
//   List<CustomerEvent> tempEvents = [];
//   Map<String, int> endtimeServer1 = {};
//   Map<String, int> endtimeServer2 = {};
//   try {
//     int customerCount = Random().nextInt(6) + 5;
//     int arrivalTime = 0;
//     for (int i = 1; i <= customerCount; i++) {
//       int interval = Random().nextInt(3) + 0;
//       arrivalTime += interval;
//       var randomServiceKey =
//           services.keys.elementAt(Random().nextInt(services.length));
//       var selectedService = services[randomServiceKey]!;
//       String durationStr = selectedService['serviceDuration'].trim();
//       int serviceDuration = int.tryParse(durationStr) ?? 0;
//       bool assignToServer1 = true;
//       if (endtimeServer1.containsKey(randomServiceKey) &&
//           endtimeServer2.containsKey(randomServiceKey)) {
//         if (endtimeServer1[randomServiceKey]! <= endtimeServer2[randomServiceKey]!) {
//           arrivalTime = max(endtimeServer1[randomServiceKey]!, arrivalTime);
//           assignToServer1 = true;
//         } else {
//           arrivalTime = max(endtimeServer2[randomServiceKey]!, arrivalTime);
//           assignToServer1 = false;
//         }
//       } else if (endtimeServer1.containsKey(randomServiceKey)) {
//         arrivalTime = max(endtimeServer1[randomServiceKey]!, arrivalTime);
//         assignToServer1 = true;
//       } else if (endtimeServer2.containsKey(randomServiceKey)) {
//         arrivalTime = max(endtimeServer2[randomServiceKey]!, arrivalTime);
//         assignToServer1 = false;
//       }
//       int departureTime = arrivalTime + serviceDuration;
//       if (assignToServer1) {
//         endtimeServer1[randomServiceKey] = departureTime;
//       } else {
//         endtimeServer2[randomServiceKey] = departureTime;
//       }
//       tempEvents.add(CustomerEvent(
//         customerId: i.toString(),
//         eventType: "Arrival",
//         clockTime: arrivalTime.toString(),
//         serviceCode: selectedService['serviceCode'],
//         serviceTitle: selectedService['serviceTitle'],
//         serviceDuration: serviceDuration.toString(),
//         endTime: departureTime.toString(),
//         serverId: assignToServer1 ? "Server 1" : "Server 2",
//       ));
//       tempEvents.add(CustomerEvent(
//         customerId: i.toString(),
//         eventType: "Departure",
//         clockTime: departureTime.toString(),
//         serviceCode: selectedService['serviceCode'],
//         serviceTitle: selectedService['serviceTitle'],
//         serviceDuration: serviceDuration.toString(),
//         endTime: departureTime.toString(),
//         serverId: assignToServer1 ? "Server 1" : "Server 2",
//       ));
//     }
//     tempEvents.sort((a, b) {
//       return int.parse(a.clockTime).compareTo(int.parse(b.clockTime));
//     });
//     currentData.clear();
//     currentData.addAll(tempEvents);
//     setState(() {
//       updateDisplays();
//     });
//     showDialog(
//       context: context,
//       builder: (context) => AlertDialog(
//         title: const Text('Simulation Complete'),
//         content: const Text('Simulation process completed successfully!'),
//         actions: [
//           TextButton(
//             onPressed: () => Navigator.of(context).pop(),
//             child: const Text('OK'),
//           ),
//         ],
//       ),
//     );
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

// void probabilitySimulation() {
  //   showProbabilityColumns = true;
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
  //     double arrivalProbability = 0.6;
  //     int maxCustomers = 20;
  //     List<CustomerEvent> simulatedData = [];
  //     int arrivalTime = 0;
  //     for (int customerId = 1; customerId <= maxCustomers; customerId++) {
  //       if (Random().nextDouble() <= arrivalProbability) {
  //         arrivalTime += Random().nextInt(3) + 1;
  //         var randomServiceKey =
  //             services.keys.elementAt(Random().nextInt(services.length));
  //         var serviceInfo = services[randomServiceKey]!;
  //         int serviceDuration =
  //             int.tryParse(serviceInfo['serviceDuration']) ?? 0;
  //         int departureTime = arrivalTime + serviceDuration;
  //         double arrivalProb = Random().nextDouble();
  //         double completionProb = Random().nextDouble();
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
  //     }
  //     simulatedData.sort((a, b) {
  //       return int.parse(a.clockTime).compareTo(int.parse(b.clockTime));
  //     });
  //     if (simulatedData.isNotEmpty) {
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
  //     } else {
  //       showDialog(
  //         context: context,
  //         builder: (context) => AlertDialog(
  //           title: const Text('No Data'),
  //           content: const Text('No events were generated in this simulation.'),
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

  // void saveAllData() async {
  //   if (currentData.isEmpty) {
  //     showDialog(
  //       context: context,
  //       builder: (context) => AlertDialog(
  //         title: const Text("Warning"),
  //         content: const Text("No data to save!"),
  //         actions: [
  //           TextButton(
  //             onPressed: () => Navigator.of(context).pop(),
  //             child: const Text("OK"),
  //           ),
  //         ],
  //       ),
  //     );
  //     return;
  //   }
  //   try {
  //     String? filePath = await FilePicker.platform.saveFile(
  //       dialogTitle: 'Save Excel File',
  //       fileName: 'simulation_data.xlsx',
  //     );
  //     if (filePath != null) {
  //       var excel = Excel.createExcel();
  //       Sheet sheet = excel['Sheet1'];
  //       sheet.appendRow([
  //         'Customer ID',
  //         'Event Type',
  //         'Clock Time',
  //         'Service Code',
  //         'Service Title',
  //         'Service Duration',
  //         'End Time'
  //       ]);
  //       for (var event in currentData) {
  //         sheet.appendRow([
  //           event.customerId,
  //           event.eventType,
  //           event.clockTime,
  //           event.serviceCode,
  //           event.serviceTitle,
  //           event.serviceDuration,
  //           event.endTime,
  //         ]);
  //       }
  //       List<int> bytes = excel.encode() ?? [];
  //       File(filePath).writeAsBytesSync(bytes);
  //       showDialog(
  //         context: context,
  //         builder: (context) => AlertDialog(
  //           title: const Text("Success"),
  //           content: const Text("Data saved successfully!"),
  //           actions: [
  //             TextButton(
  //               onPressed: () => Navigator.of(context).pop(),
  //               child: const Text("OK"),
  //             ),
  //           ],
  //         ),
  //       );
  //     }
  //   } catch (e) {
  //     showDialog(
  //       context: context,
  //       builder: (context) => AlertDialog(
  //         title: const Text("Error"),
  //         content: Text("Failed to save data: ${e.toString()}"),
  //         actions: [
  //           TextButton(
  //             onPressed: () => Navigator.of(context).pop(),
  //             child: const Text("OK"),
  //           ),
  //         ],
  //       ),
  //     );
  //   }
  // }

// void clearAllData() {
  //   showDialog(
  //     context: context,
  //     builder: (BuildContext context) {
  //       return AlertDialog(
  //         title: const Text("Confirm Clear"),
  //         content: const Text("Are you sure you want to clear all data?"),
  //         actions: [
  //           TextButton(
  //             onPressed: () {
  //               setState(() {
  //                 newData.clear();
  //                 currentData.clear();
  //                 services.clear();
  //                 graphDataPoints.clear();
  //               });
  //               Navigator.of(context).pop(); // Close the dialog
  //             },
  //             child: const Text("Yes"),
  //           ),
  //           TextButton(
  //             onPressed: () {
  //               Navigator.of(context).pop(); // Close the dialog
  //             },
  //             child: const Text("No"),
  //           ),
  //         ],
  //       );
  //     },
  //   );
  // }

  // void _addService() {
  //   final serviceCode = serviceCodeController.text;
  //   final serviceTitle = serviceTitleController.text;
  //   final serviceDuration = serviceDurationController.text;
  //   if (serviceCode.isNotEmpty &&
  //       serviceTitle.isNotEmpty &&
  //       serviceDuration.isNotEmpty) {
  //     services[serviceCode] = {
  //       'serviceCode': serviceCode,
  //       'serviceTitle': serviceTitle,
  //       'serviceDuration': serviceDuration,
  //     };
  //     print("Service Added: $serviceCode - $serviceTitle");
  //     serviceCodeController.clear();
  //     serviceTitleController.clear();
  //     serviceDurationController.clear();
  //   }
  // }

// Widget buildGraphDisplay() {
  //   return Container(
  //     height: 300, // Adjust as needed for visibility
  //     width: double.infinity,
  //     decoration: BoxDecoration(
  //       color: Colors.grey[200], // Subtle background color
  //       borderRadius: BorderRadius.circular(10),
  //     ),
  //     child: LineChart(
  //       LineChartData(
  //         lineBarsData: [
  //           LineChartBarData(
  //             spots: graphDataPoints,
  //             isCurved: true, // Add smooth curves
  //             gradient: const LinearGradient(
  //               colors: [Colors.blueAccent, Colors.lightBlue],
  //               begin: Alignment.topCenter,
  //               end: Alignment.bottomCenter,
  //             ), // Apply gradient to the line
  //             belowBarData: BarAreaData(
  //               show: true,
  //               gradient: LinearGradient(
  //                 colors: [
  //                   Colors.blueAccent.withOpacity(0.3),
  //                   Colors.lightBlue.withOpacity(0.0)
  //                 ],
  //                 begin: Alignment.topCenter,
  //                 end: Alignment.bottomCenter,
  //               ),
  //             ), // Show gradient fill below the line
  //             dotData: FlDotData(
  //               show: true,
  //               getDotPainter: (spot, percent, barData, index) {
  //                 return FlDotCirclePainter(
  //                   radius: 4,
  //                   color: Colors.redAccent, // Customize dot color
  //                   strokeWidth: 2,
  //                   strokeColor: Colors.blueAccent,
  //                 );
  //               },
  //             ),
  //             isStrokeCapRound: true,
  //             barWidth: 3, // Thicker line width
  //           ),
  //         ],
  //         gridData: FlGridData(
  //           show: true,
  //           drawVerticalLine: true,
  //           verticalInterval: 1,
  //           horizontalInterval: 1,
  //           getDrawingVerticalLine: (value) => FlLine(
  //             color: Colors.grey.withOpacity(0.3),
  //             strokeWidth: 1,
  //             dashArray: [5, 5], // Dashed vertical lines
  //           ),
  //           getDrawingHorizontalLine: (value) => FlLine(
  //             color: Colors.grey.withOpacity(0.3),
  //             strokeWidth: 1,
  //             dashArray: [5, 5], // Dashed horizontal lines
  //           ),
  //         ),
  //         titlesData: FlTitlesData(
  //           leftTitles: AxisTitles(
  //             sideTitles: SideTitles(
  //               showTitles: true,
  //               reservedSize: 30,
  //               getTitlesWidget: (value, meta) {
  //                 return Padding(
  //                   padding: const EdgeInsets.only(right: 8.0),
  //                   child: Text(
  //                     value.toInt().toString(),
  //                     style: const TextStyle(color: Colors.blueAccent),
  //                   ),
  //                 ); // Display customer ID on the y-axis
  //               },
  //             ),
  //           ),
  //           bottomTitles: AxisTitles(
  //             sideTitles: SideTitles(
  //               showTitles: true,
  //               reservedSize: 30,
  //               getTitlesWidget: (value, meta) {
  //                 return Padding(
  //                   padding: const EdgeInsets.only(top: 8.0),
  //                   child: Text(
  //                     value.toInt().toString(),
  //                     style: const TextStyle(color: Colors.blueAccent),
  //                   ),
  //                 ); // Display clock time on the x-axis
  //               },
  //             ),
  //           ),
  //           topTitles: AxisTitles(
  //             sideTitles: SideTitles(showTitles: false),
  //           ),
  //           rightTitles: AxisTitles(
  //             sideTitles: SideTitles(showTitles: false),
  //           ),
  //         ),
  //         borderData: FlBorderData(
  //           show: true,
  //           border: box_border.Border.all(
  //             color: Colors.blueAccent,
  //             width: 1,
  //           ),
  //         ),
  //       ),
  //     ),
  //   );
  // }