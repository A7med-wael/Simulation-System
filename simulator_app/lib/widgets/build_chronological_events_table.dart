import 'package:flutter/material.dart';
import 'package:simulator_app/models/customer_event.dart';

Widget buildChronologicalEventsTable(
    {required List<CustomerEvent> currentData,required bool showProbabilityColumns}) {
  return Padding(
    padding: const EdgeInsets.all(10.0),
    child: Column(
      children: [
        const Text(
          'Chronological Order of Events',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: DataTable(
            columns: [
              const DataColumn(label: Text('ID')),
              const DataColumn(label: Text('Time')),
              const DataColumn(label: Text('Event Type')),
              const DataColumn(label: Text('Details')),
              if (showProbabilityColumns)
                const DataColumn(label: Text('Arrival Probability')),
              if (showProbabilityColumns)
                const DataColumn(label: Text('Completion Probability')),
            ],
            rows: currentData
                .map((event) => DataRow(cells: [
                      DataCell(Text(event.customerId)),
                      DataCell(Text(event.clockTime)),
                      DataCell(Text(event.eventType)),
                      DataCell(Text(event.serviceTitle)),
                      if (showProbabilityColumns)
                        DataCell(Text(event.arrivalProb)),
                      if (showProbabilityColumns)
                        DataCell(Text(event.completionProb)),
                    ]))
                .toList(),
          ),
        ),
      ],
    ),
  );
}
