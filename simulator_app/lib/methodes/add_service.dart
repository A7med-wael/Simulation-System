import 'package:flutter/material.dart';

void addService({
  required TextEditingController serviceCodeController,
  required TextEditingController serviceTitleController,
  required TextEditingController serviceDurationController,
  required Map<String, Map<String, dynamic>> services,
}) {
  final serviceCode = serviceCodeController.text;
  final serviceTitle = serviceTitleController.text;
  final serviceDuration = serviceDurationController.text;

  if (serviceCode.isNotEmpty &&
      serviceTitle.isNotEmpty &&
      serviceDuration.isNotEmpty) {
    services[serviceCode] = {
      'serviceCode': serviceCode,
      'serviceTitle': serviceTitle,
      'serviceDuration': serviceDuration,
    };
    print("Service Added: $serviceCode - $serviceTitle");

    serviceCodeController.clear();
    serviceTitleController.clear();
    serviceDurationController.clear();
  }
}
