import 'package:flutter/material.dart';

Widget buildCustomerDataTable({
  required List<Map<String, dynamic>> newData,
  required bool showProbabilityColumns,
  required bool showParallelColumns,
}) {
  return Column(
    children: [
      SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: DataTable(
          columns: [
            const DataColumn(
                label: Text(
              'Customer ID',
              style: TextStyle(color: Colors.white),
            )),
            const DataColumn(
                label: Text(
              'Event Type',
              style: TextStyle(color: Colors.white),
            )),
            const DataColumn(
                label: Text(
              'Clock Time',
              style: TextStyle(color: Colors.white),
            )),
            const DataColumn(
                label: Text(
              'Service Code',
              style: TextStyle(color: Colors.white),
            )),
            const DataColumn(
                label: Text(
              'Service Title',
              style: TextStyle(color: Colors.white),
            )),
            const DataColumn(
                label: Text(
              'Service Duration',
              style: TextStyle(color: Colors.white),
            )),
            const DataColumn(
                label: Text(
              'End Time',
              style: TextStyle(color: Colors.white),
            )),
            if (showParallelColumns)
              const DataColumn(
                  label: Text(
                "Server",
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
          rows: newData
              .map((data) => DataRow(cells: [
                    DataCell(Text(
                      data['Customer ID'].toString(),
                      style: TextStyle(color: Colors.white),
                    )),
                    DataCell(Text(
                      data['Event Type'].toString(),
                      style: TextStyle(color: Colors.white),
                    )),
                    DataCell(Text(
                      data['Clock Time'].toString(),
                      style: TextStyle(color: Colors.white),
                    )),
                    DataCell(Text(
                      data['Service Code'].toString(),
                      style: TextStyle(color: Colors.white),
                    )),
                    DataCell(Text(
                      data['Service Title'].toString(),
                      style: TextStyle(color: Colors.white),
                    )),
                    DataCell(Text(
                      data['Service Duration'].toString(),
                      style: TextStyle(color: Colors.white),
                    )),
                    DataCell(Text(
                      data['End Time'].toString(),
                      style: TextStyle(color: Colors.white),
                    )),
                    if (showParallelColumns)
                      DataCell(Text(
                        data['Server'].toString(),
                        style: TextStyle(color: Colors.white),
                      )),
                    if (showProbabilityColumns)
                      DataCell(Text(
                        data['Arrival Probability'].toString(),
                        style: TextStyle(color: Colors.white),
                      )),
                    if (showProbabilityColumns)
                      DataCell(Text(
                        data['Completion Probability'].toString(),
                        style: TextStyle(color: Colors.white),
                      )),
                  ]))
              .toList(),
        ),
      ),
    ],
  );
}
