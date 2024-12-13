import 'dart:io';
import 'package:excel/excel.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:simulator_app/models/customer_event.dart';

void saveAllData({
  required List<CustomerEvent> currentData,
  required BuildContext context,
}) async {
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
