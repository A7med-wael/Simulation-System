import 'package:flutter/material.dart';
import 'package:simulator_app/models/customer_event.dart';

Widget buildChronologicalEventsTable(
    {required List<CustomerEvent> currentData,
    required bool showProbabilityColumns}) {
  return Padding(
    padding: const EdgeInsets.all(10.0),
    child: Column(
      children: [
        SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: DataTable(
            columns: [
              const DataColumn(
                  label: Text(
                'ID',
                style: TextStyle(color: Colors.white),
              )),
              const DataColumn(
                  label: Text(
                'Time',
                style: TextStyle(color: Colors.white),
              )),
              const DataColumn(
                  label: Text(
                'Event Type',
                style: TextStyle(color: Colors.white),
              )),
              const DataColumn(
                  label: Text(
                'Details',
                style: TextStyle(color: Colors.white),
              )),
              if (showProbabilityColumns)
                const DataColumn(
                    label: Text(
                  'Arrival Probability',
                  style: TextStyle(color: Colors.white),
                )),
              if (showProbabilityColumns)
                const DataColumn(
                    label: Text(
                  'Completion Probability',
                  style: TextStyle(color: Colors.white),
                )),
            ],
            rows: currentData
                .map((event) => DataRow(cells: [
                      DataCell(Text(
                        event.customerId,
                        style: TextStyle(color: Colors.white),
                      )),
                      DataCell(Text(
                        event.clockTime,
                        style: TextStyle(color: Colors.white),
                      )),
                      DataCell(Text(
                        event.eventType,
                        style: TextStyle(color: Colors.white),
                      )),
                      DataCell(Text(
                        event.serviceTitle,
                        style: TextStyle(color: Colors.white),
                      )),
                      if (showProbabilityColumns)
                        DataCell(Text(
                          event.arrivalProb,
                          style: TextStyle(color: Colors.white),
                        )),
                      if (showProbabilityColumns)
                        DataCell(Text(
                          event.completionProb,
                          style: TextStyle(color: Colors.white),
                        )),
                    ]))
                .toList(),
          ),
        ),
      ],
    ),
  );
}
