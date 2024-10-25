import 'package:flutter/material.dart';
import 'package:simulator_app/constents.dart';

class CustomButton extends StatelessWidget {
  const CustomButton({super.key, required this.onPressed, required this.text});

  final VoidCallback onPressed;
  final String text;
  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      style: const ButtonStyle(
        fixedSize: WidgetStatePropertyAll(
          Size(160, 40),
        ),
        backgroundColor: WidgetStatePropertyAll(
          PrimaryColor,
        ),
      ),
      onPressed: onPressed,
      child: Text(
        text,
        style: const TextStyle(
          color: Colors.white,
          fontSize: 20,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}
