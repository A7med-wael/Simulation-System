import 'dart:io';
import 'package:excel/excel.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

import '../widgets/custom_dilog.dart';

Future<void> initializeData({
  required BuildContext context,
  required Map<String, Map<String, dynamic>> services,
  required VoidCallback onSuccess,
}) async {
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
          if (row.isNotEmpty) {
            var serviceCode = row[0]?.value;
            var serviceTitle = row[1]?.value;
            var serviceDuration = row[2]?.value;

            if (serviceCode != null &&
                serviceTitle != null &&
                serviceDuration != null) {
              services[serviceCode.toString()] = {
                'serviceCode': serviceCode.toString(),
                'serviceTitle': serviceTitle.toString(),
                'serviceDuration': serviceDuration.toString(),
              };
            }
          }
        }
      }
      onSuccess();
      CustomDialog.showCustomDialog(
        dialogType: DialogType.Success,
        context: context,
        title: 'File Loaded successfully',
        description: '',
      );
      // showDialog(
      //   context: context,
      //   builder: (context) => AlertDialog(
      //     title: const Text('File Loaded'),
      //     content: const Text('File loaded successfully.'),
      //     actions: [
      //       TextButton(onPressed: () => Navigator.of(context).pop(), child: const Text('OK')),
      //     ],
      //   ),
      // );
    } catch (e) {
      print('Error while processing Excel file: $e');
    }
  } else {
    print('No file selected');
  }
}
