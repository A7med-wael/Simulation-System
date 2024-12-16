import 'dart:math';
import 'package:flutter/material.dart';
import 'package:simulator_app/models/customer_event.dart';
import 'package:simulator_app/widgets/custom_dilog.dart';

void simulateOneServer({
  required Map<String, Map<String, dynamic>> services,
  required List<CustomerEvent> currentData,
  required BuildContext context,
  required VoidCallback updateDisplays,
}) {
  if (services.isEmpty) {
    CustomDialog.showCustomDialog(
        context: context,
        title: "Error",
        description:
            'No services available! Please add services first or upload an Excel file.',
        dialogType: DialogType.Failure);
    // CustomDialog.showCustomDialog(
    //   context: context,
    //   title: "Error",
    // description:
    //     'No services available! Please add services first or upload an Excel file.',
    // );
    // showDialog(
    //   context: context,
    //   builder: (context) => AlertDialog(
    //     title: const Text('Error'),
    //     content: const Text(
    //         'No services available! Please add services first or upload an Excel file.'),
    //     actions: [
    //       TextButton(
    //         onPressed: () => Navigator.of(context).pop(),
    //         child: const Text('OK'),
    //       ),
    //     ],
    //   ),
    // );
    return;
  }

  List<CustomerEvent> tempEvents = [];
  Map<String, dynamic> endtime = {};

  try {
    int customerCount = Random().nextInt(6) + 5;
    int arrivalTime = 0;

    for (int i = 1; i <= customerCount; i++) {
      int interval = Random().nextInt(3) + 0;
      arrivalTime += interval;

      var randomServiceKey =
          services.keys.elementAt(Random().nextInt(services.length));
      var selectedService = services[randomServiceKey]!;
      String durationStr = selectedService['serviceDuration'].trim();
      int serviceDuration = int.tryParse(durationStr) ?? 0;

      if (endtime.containsKey(randomServiceKey)) {
        arrivalTime = max(endtime[randomServiceKey]!, arrivalTime);
      }

      int departureTime = arrivalTime + serviceDuration;
      endtime[randomServiceKey] = departureTime;

      tempEvents.add(CustomerEvent(
        customerId: i.toString(),
        eventType: "Arrival",
        clockTime: arrivalTime.toString(),
        serviceCode: selectedService['serviceCode'],
        serviceTitle: selectedService['serviceTitle'],
        serviceDuration: serviceDuration.toString(),
        endTime: departureTime.toString(),
      ));

      tempEvents.add(CustomerEvent(
        customerId: i.toString(),
        eventType: "Departure",
        clockTime: departureTime.toString(),
        serviceCode: selectedService['serviceCode'],
        serviceTitle: selectedService['serviceTitle'],
        serviceDuration: serviceDuration.toString(),
        endTime: departureTime.toString(),
      ));
    }

    tempEvents.sort((a, b) {
      return int.parse(a.clockTime).compareTo(int.parse(b.clockTime));
    });

    currentData.clear();
    currentData.addAll(tempEvents);

    updateDisplays();
    CustomDialog.showCustomDialog(
      dialogType: DialogType.Success,
      context: context,
      title: "Simulation Complete",
      description: 'Simulation process completed successfully!',
    );
    // showDialog(
    //   context: context,
    //   builder: (context) => AlertDialog(
    //     title: const Text('Simulation Complete'),
    //     content: const Text('Simulation process completed successfully!'),
    //     actions: [
    //       TextButton(
    //         onPressed: () => Navigator.of(context).pop(),
    //         child: const Text('OK'),
    //       ),
    //     ],
    //   ),
    // );
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
