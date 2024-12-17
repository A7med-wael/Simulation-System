
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';

import 'pages/home_page.dart';

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