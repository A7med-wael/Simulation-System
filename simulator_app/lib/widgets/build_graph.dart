import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/painting/box_border.dart' as box_border;

class BuildGraph extends StatefulWidget {
  const BuildGraph({super.key,});
  @override
  State<BuildGraph> createState() => _BuildGraphState();
}

class _BuildGraphState extends State<BuildGraph> {
  
  List<FlSpot> graphDataPoints = [];
  @override
  Widget build(BuildContext context) {
    return Container(
      height: 300, // Adjust as needed for visibility
      width: double.infinity,
      decoration: BoxDecoration(
        color: Colors.grey[200], // Subtle background color
        borderRadius: BorderRadius.circular(10),
      ),
      child: LineChart(
        LineChartData(
          lineBarsData: [
            LineChartBarData(
              spots: graphDataPoints,
              isCurved: true, // Add smooth curves
              gradient: const LinearGradient(
                colors: [Colors.blueAccent, Colors.lightBlue],
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
              ), // Apply gradient to the line
              belowBarData: BarAreaData(
                show: true,
                gradient: LinearGradient(
                  colors: [
                    Colors.blueAccent.withOpacity(0.3),
                    Colors.lightBlue.withOpacity(0.0)
                  ],
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                ),
              ), // Show gradient fill below the line
              dotData: FlDotData(
                show: true,
                getDotPainter: (spot, percent, barData, index) {
                  return FlDotCirclePainter(
                    radius: 4,
                    color: Colors.redAccent, // Customize dot color
                    strokeWidth: 2,
                    strokeColor: Colors.blueAccent,
                  );
                },
              ),
              isStrokeCapRound: true,
              barWidth: 3, // Thicker line width
            ),
          ],
          gridData: FlGridData(
            show: true,
            drawVerticalLine: true,
            verticalInterval: 1,
            horizontalInterval: 1,
            getDrawingVerticalLine: (value) => FlLine(
              color: Colors.grey.withOpacity(0.3),
              strokeWidth: 1,
              dashArray: [5, 5], // Dashed vertical lines
            ),
            getDrawingHorizontalLine: (value) => FlLine(
              color: Colors.grey.withOpacity(0.3),
              strokeWidth: 1,
              dashArray: [5, 5], // Dashed horizontal lines
            ),
          ),
          titlesData: FlTitlesData(
            leftTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                reservedSize: 30,
                getTitlesWidget: (value, meta) {
                  return Padding(
                    padding: const EdgeInsets.only(right: 8.0),
                    child: Text(
                      value.toInt().toString(),
                      style: const TextStyle(color: Colors.blueAccent),
                    ),
                  ); // Display customer ID on the y-axis
                },
              ),
            ),
            bottomTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                reservedSize: 30,
                getTitlesWidget: (value, meta) {
                  return Padding(
                    padding: const EdgeInsets.only(top: 8.0),
                    child: Text(
                      value.toInt().toString(),
                      style: const TextStyle(color: Colors.blueAccent),
                    ),
                  ); // Display clock time on the x-axis
                },
              ),
            ),
            topTitles: AxisTitles(
              sideTitles: SideTitles(showTitles: false),
            ),
            rightTitles: AxisTitles(
              sideTitles: SideTitles(showTitles: false),
            ),
          ),
          borderData: FlBorderData(
            show: true,
            border: box_border.Border.all(
              color: Colors.blueAccent,
              width: 1,
            ),
          ),
        ),
      ),
    );
  }
}
