import 'package:flutter/material.dart';
import 'package:simulator_app/widgets/custom_button.dart';

Widget buildServiceForm({
  required TextEditingController codeController,
  required TextEditingController titleController,
  required TextEditingController durationController,
  required VoidCallback onAddService,
}) {
  return Container(
    padding: const EdgeInsets.all(10),
    decoration: BoxDecoration(
      borderRadius: BorderRadius.circular(10),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Center(
          child: Text('Add New Service',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
        ),
        const SizedBox(height: 10),
        buildTextInputField(controller: codeController, labelText: 'Service Code:'),
        buildTextInputField(controller: titleController, labelText: 'Service Title:'),
        buildTextInputField(
          controller: durationController,
          labelText: 'Duration (min):',
          keyboardType: TextInputType.number,
        ),
        const SizedBox(height: 10),
        Center(
          child: CustomButton(onPressed: onAddService, text: 'Add Service'),
        ),
      ],
    ),
  );
}

Widget buildTextInputField({
  required TextEditingController controller,
  required String labelText,
  TextInputType keyboardType = TextInputType.text,
}) {
  return Padding(
    padding: const EdgeInsets.only(bottom: 10),
    child: TextFormField(
      controller: controller,
      decoration: InputDecoration(
        labelText: labelText,
        border: const OutlineInputBorder(),
      ),
      keyboardType: keyboardType,
    ),
  );
}
