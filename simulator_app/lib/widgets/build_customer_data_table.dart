import 'package:flutter/material.dart';

Widget buildCustomerDataTable(
    {required List<Map<String, dynamic>> newData,required bool showProbabilityColumns}) {
  return Column(
    children: [
      const Text(
        'Customer Data Table',
        style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
      ),
      SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: DataTable(
          columns: [
            const DataColumn(label: Text('Customer ID')),
            const DataColumn(label: Text('Event Type')),
            const DataColumn(label: Text('Clock Time')),
            const DataColumn(label: Text('Service Code')),
            const DataColumn(label: Text('Service Title')),
            const DataColumn(label: Text('Service Duration')),
            const DataColumn(label: Text('End Time')),
            if (showProbabilityColumns)
              const DataColumn(label: Text('Arrival Probability')),
            if (showProbabilityColumns)
              const DataColumn(label: Text('Completion Probability')),
          ],
          rows: newData
              .map((data) => DataRow(cells: [
                    DataCell(Text(data['Customer ID'].toString())),
                    DataCell(Text(data['Event Type'].toString())),
                    DataCell(Text(data['Clock Time'].toString())),
                    DataCell(Text(data['Service Code'].toString())),
                    DataCell(Text(data['Service Title'].toString())),
                    DataCell(Text(data['Service Duration'].toString())),
                    DataCell(Text(data['End Time'].toString())),
                    if (showProbabilityColumns)
                      DataCell(Text(data['Arrival Probability'].toString())),
                    if (showProbabilityColumns)
                      DataCell(Text(data['Completion Probability'].toString())),
                  ]))
              .toList(),
        ),
      ),
    ],
  );
}
