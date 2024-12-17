import 'dart:io';
import 'package:excel/excel.dart';
import 'package:path_provider/path_provider.dart';
import 'package:flutter/material.dart';
import '../models/customer_event.dart';
import '../widgets/custom_dilog.dart';

void saveAllData({
  required List<CustomerEvent> currentData,
  required BuildContext context,
}) async {
  if (currentData.isEmpty) {
    CustomDialog.showCustomDialog(
      dialogType: DialogType.Failure,
      context: context,
      title: "Warning",
      description: "No data to save!",
    );
    return;
  }

  try {
    // Get the documents directory
    final directory = await getApplicationDocumentsDirectory();
    final String filePath = '${directory.path}/simulation_data.xlsx';

    // Create an Excel file
    var excel = Excel.createExcel();
    Sheet sheet = excel['Sheet1'];

    // Add headers
    sheet.appendRow([
      'Customer ID',
      'Event Type',
      'Clock Time',
      'Service Code',
      'Service Title',
      'Service Duration',
      'End Time'
    ]);

    // Add data rows
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

    // Save the Excel file
    List<int> bytes = excel.encode() ?? [];
    File(filePath).writeAsBytesSync(bytes);

    CustomDialog.showCustomDialog(
      dialogType: DialogType.Success,
      context: context,
      title: "Success",
      description: "Data saved to: $filePath",
    );
  } catch (e) {
    CustomDialog.showCustomDialog(
      dialogType: DialogType.Failure,
      context: context,
      title: 'Error',
      description: "Failed to save data: ${e.toString()}",
    );
  }
}
