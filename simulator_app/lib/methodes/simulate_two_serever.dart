import 'dart:math';
import 'package:flutter/material.dart';
import 'package:simulator_app/models/customer_event.dart';

void simulateTwoServers({
  required Map<String, Map<String, dynamic>> services,
  required List<CustomerEvent> currentData,
  required BuildContext context,
  required VoidCallback updateDisplays,
}) {
  if (services.isEmpty) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Error'),
        content: const Text('No services available! Please add services first or upload an Excel file.'),
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

  List<CustomerEvent> tempEvents = [];
  Map<String, dynamic> endtimeServer1 = {};
  Map<String, dynamic> endtimeServer2 = {};

  try {
    int customerCount = Random().nextInt(6) + 5; // Generate between 5 and 10 customers
    int arrivalTime = 0;

    for (int i = 1; i <= customerCount; i++) {
      int interval = Random().nextInt(3) + 1; // Random interval between arrivals
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
      } else if (!endtimeServer2.containsKey(randomServiceKey) ||
          (endtimeServer2[randomServiceKey]! <= arrivalTime)) {
        // Assign to Server 2
        serverAssigned = "Server 2";
        endtimeServer2[randomServiceKey] = arrivalTime + serviceDuration;
        serverEnd = endtimeServer2[randomServiceKey]!;
      } else {
        // Both servers busy; assign to the one that becomes available first
        if (endtimeServer1[randomServiceKey]! <= endtimeServer2[randomServiceKey]!) {
          serverAssigned = "Server 1";
          arrivalTime = endtimeServer1[randomServiceKey]!;
          endtimeServer1[randomServiceKey] = arrivalTime + serviceDuration;
          serverEnd = endtimeServer1[randomServiceKey]!;
        } else {
          serverAssigned = "Server 2";
          arrivalTime = endtimeServer2[randomServiceKey]!;
          endtimeServer2[randomServiceKey] = arrivalTime + serviceDuration;
          serverEnd = endtimeServer2[randomServiceKey]!;
        }
      }

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

    updateDisplays();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Simulation Complete'),
        content: const Text('Simulation with two servers completed successfully!'),
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
