import 'package:flutter/material.dart';
import 'package:simulator_app/pages/home_page.dart';

void main() {
  runApp(
    SimulationClockTable(),
  );
}

class SimulationClockTable extends StatelessWidget {
  const SimulationClockTable({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomePage(),
    );
  }
}
