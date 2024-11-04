import 'package:flutter/material.dart';

import 'pages/home_page.dart';

void main() {
  runApp(
    const SimulationClockTable(),
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
//      push
// git add .
// git commit -m "commit message"
// git push






// git fetch
// git merge flutterApp