import 'package:flutter/material.dart';
import 'package:simulator_app/widgets/custom_button.dart';

Widget buildActionButtons({
  required VoidCallback onUploadFile,
  required VoidCallback onSimulate,
  required VoidCallback onProbability,
}) {
  return Column(
    children: [
      CustomButton(onPressed: onUploadFile, text: 'Upload File'),
      CustomButton(onPressed: onSimulate, text: 'Simulate'),
      CustomButton(onPressed: onProbability, text: 'Probability',),
    ],
  );
}
