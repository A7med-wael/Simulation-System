import 'dart:math';
import 'package:flutter/material.dart';
import 'package:simulator_app/models/customer_event.dart';
import '../widgets/custom_dilog.dart';

void simulateTwoServers({
  required Map<String, Map<String, dynamic>> services,
  required List<CustomerEvent> currentData,
  required BuildContext context,
  required VoidCallback updateDisplays,
}) {
  if (services.isEmpty) {
    CustomDialog.showCustomDialog(
      dialogType: DialogType.Failure,
      context: context,
      title: 'Error',
      description:
          'No services available! Please add services first or upload an Excel file.',
    );

    return;
  }

  List<CustomerEvent> tempEvents = [];
  Map<String, dynamic> endtimeServer1 = {};
  Map<String, dynamic> endtimeServer2 = {};

  // Statistics trackers
  int totalServiceTimeServer1 = 0;
  int totalServiceTimeServer2 = 0;
  int totalCustomersServer1 = 0;
  int totalCustomersServer2 = 0;
  int totalWaitingTime = 0;
  int totalCustomers = 0;

  try {
    int customerCount =
        Random().nextInt(6) + 5; // Generate between 5 and 10 customers
    int arrivalTime = 0;

    for (int i = 1; i <= customerCount; i++) {
      int interval =
          Random().nextInt(3) + 1; // Random interval between arrivals
      arrivalTime += interval;

      var randomServiceKey =
          services.keys.elementAt(Random().nextInt(services.length));
      var selectedService = services[randomServiceKey]!;
      String durationStr = selectedService['serviceDuration'].trim();
      int serviceDuration = int.tryParse(durationStr) ?? 0;

      // Determine which server to assign based on availability
      String serverAssigned;
      int serverEnd;

      if (!endtimeServer1.containsKey(randomServiceKey) ||
          (endtimeServer1[randomServiceKey]! <= arrivalTime)) {
        // Assign to Server 1
        serverAssigned = "Server 1";
        endtimeServer1[randomServiceKey] = arrivalTime + serviceDuration;
        serverEnd = endtimeServer1[randomServiceKey]!;

        totalServiceTimeServer1 += serviceDuration;
        totalCustomersServer1++;
      } else if (!endtimeServer2.containsKey(randomServiceKey) ||
          (endtimeServer2[randomServiceKey]! <= arrivalTime)) {
        // Assign to Server 2
        serverAssigned = "Server 2";
        endtimeServer2[randomServiceKey] = arrivalTime + serviceDuration;
        serverEnd = endtimeServer2[randomServiceKey]!;

        totalServiceTimeServer2 += serviceDuration;
        totalCustomersServer2++;
      } else {
        // Both servers busy; assign to the one that becomes available first
        if (endtimeServer1[randomServiceKey]! <=
            endtimeServer2[randomServiceKey]!) {
          serverAssigned = "Server 1";
          totalWaitingTime +=
              (endtimeServer1[randomServiceKey]! - arrivalTime) as int;
          arrivalTime = endtimeServer1[randomServiceKey]!;

          endtimeServer1[randomServiceKey] = arrivalTime + serviceDuration;
          serverEnd = endtimeServer1[randomServiceKey]!;

          totalServiceTimeServer1 += serviceDuration;
          totalCustomersServer1++;
        } else {
          serverAssigned = "Server 2";
          totalWaitingTime +=
              (endtimeServer2[randomServiceKey]! - arrivalTime) as int;
          arrivalTime = endtimeServer2[randomServiceKey]!;

          endtimeServer2[randomServiceKey] = arrivalTime + serviceDuration;
          serverEnd = endtimeServer2[randomServiceKey]!;

          totalServiceTimeServer2 += serviceDuration;
          totalCustomersServer2++;
        }
      }

      // Increment total customer count
      totalCustomers++;

      // Add customer arrival and departure events
      tempEvents.add(CustomerEvent(
        customerId: i.toString(),
        eventType: "Arrival",
        clockTime: arrivalTime.toString(),
        serviceCode: selectedService['serviceCode'],
        serviceTitle: selectedService['serviceTitle'],
        serviceDuration: serviceDuration.toString(),
        endTime: serverEnd.toString(),
        server: serverAssigned,
      ));

      tempEvents.add(CustomerEvent(
        customerId: i.toString(),
        eventType: "Departure",
        clockTime: serverEnd.toString(),
        serviceCode: selectedService['serviceCode'],
        serviceTitle: selectedService['serviceTitle'],
        serviceDuration: serviceDuration.toString(),
        endTime: serverEnd.toString(),
        server: serverAssigned,
      ));
    }

    tempEvents.sort((a, b) {
      return int.parse(a.clockTime).compareTo(int.parse(b.clockTime));
    });

    currentData.clear();
    currentData.addAll(tempEvents);

    // Final statistics
    double averageServiceTimeServer1 = totalCustomersServer1 == 0
        ? 0
        : totalServiceTimeServer1 / totalCustomersServer1;
    double averageServiceTimeServer2 = totalCustomersServer2 == 0
        ? 0
        : totalServiceTimeServer2 / totalCustomersServer2;
    double averageWaitingTime =
        totalCustomers == 0 ? 0 : totalWaitingTime / totalCustomers;

    updateDisplays();

    // Show success dialog with statistics
    CustomDialog.showCustomDialog(
      dialogType: DialogType.Success,
      context: context,
      title: 'Simulation Complete',
      description: '''
Simulation with two servers completed successfully!

 Statistics : 
Total Customers: $totalCustomers
Server 1:
- Total Customers: $totalCustomersServer1
- Average Service Time: ${averageServiceTimeServer1.toStringAsFixed(2)} units

Server 2:
- Total Customers: $totalCustomersServer2
- Average Service Time: ${averageServiceTimeServer2.toStringAsFixed(2)} units

Overall:
- Average Waiting Time: ${averageWaitingTime.toStringAsFixed(2)} units
''',
    );
  } catch (e) {
    CustomDialog.showCustomDialog(
      dialogType: DialogType.Failure,
      context: context,
      title: 'Error',
      description: 'Failed to generate customers: $e',
    );
  }
}
