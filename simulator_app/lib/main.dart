import 'package:flutter/material.dart';

import 'pages/home_page.dart';

void main() {
  runApp(
    SimulationClockTable(),
  );
}

class SimulationClockTable extends StatelessWidget {
  const SimulationClockTable({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomePage(),
    );
  }
}
