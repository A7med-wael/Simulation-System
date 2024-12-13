import 'dart:math';
import 'package:flutter/material.dart';
import 'package:simulator_app/models/customer_event.dart';

void probabilitySimulation({
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
    double arrivalProbability = 0.6;
    int maxCustomers = 20;
    List<CustomerEvent> simulatedData = [];
    int arrivalTime = 0;

    for (int customerId = 1; customerId <= maxCustomers; customerId++) {
      if (Random().nextDouble() <= arrivalProbability) {
        arrivalTime += Random().nextInt(3) + 1;

        var randomServiceKey =
            services.keys.elementAt(Random().nextInt(services.length));
        var serviceInfo = services[randomServiceKey]!;
        int serviceDuration = int.tryParse(serviceInfo['serviceDuration']) ?? 0;
        int departureTime = arrivalTime + serviceDuration;

        double arrivalProb = Random().nextDouble();
        double completionProb = Random().nextDouble();

        simulatedData.add(
          CustomerEvent(
            customerId: customerId.toString(),
            eventType: 'Arrival',
            clockTime: arrivalTime.toString(),
            serviceCode: serviceInfo['serviceCode'],
            serviceTitle: serviceInfo['serviceTitle'],
            serviceDuration: serviceDuration.toString(),
            endTime: departureTime.toString(),
            arrivalProb: arrivalProb.toStringAsFixed(2),
            completionProb: completionProb.toStringAsFixed(2),
          ),
        );

        simulatedData.add(
          CustomerEvent(
            customerId: customerId.toString(),
            eventType: 'Departure',
            clockTime: departureTime.toString(),
            serviceCode: serviceInfo['serviceCode'],
            serviceTitle: serviceInfo['serviceTitle'],
            serviceDuration: serviceDuration.toString(),
            endTime: departureTime.toString(),
            arrivalProb: arrivalProb.toStringAsFixed(2),
            completionProb: completionProb.toStringAsFixed(2),
          ),
        );
      }
    }

    simulatedData.sort((a, b) {
      return int.parse(a.clockTime).compareTo(int.parse(b.clockTime));
    });

    currentData.clear();
    currentData.addAll(simulatedData);
    updateDisplays();

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Probability Simulation Complete'),
        content:
            const Text('Probability-based simulation completed successfully!'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }
  catch (e) {
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