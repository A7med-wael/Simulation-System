import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:simulator_app/models/customer_event.dart';

void clearAllData({
  required Map<String, Map<String, dynamic>> services,
  required List<CustomerEvent> currentData,
  required BuildContext context,
  required List<Map<String, dynamic>> newData,
  required List<FlSpot> graphDataPoints,
  required VoidCallback updateDisplays,
}) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text("Confirm Clear"),
          content: const Text("Are you sure you want to clear all data?"),
          actions: [
            TextButton(
              onPressed: () {
                newData.clear();
                  currentData.clear();
                  services.clear();
                  graphDataPoints.clear();
                  updateDisplays();
               
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