import 'dart:ui';

import 'package:flutter/material.dart';

class CropRoadPage extends StatefulWidget {
  @override
  _CropRoadPageState createState() => _CropRoadPageState();
}

class _CropRoadPageState extends State<CropRoadPage>
    with SingleTickerProviderStateMixin {
  List<String> steps = [
    "Prepare the land by plowing and leveling.",
    "Select high-quality rice seeds.",
    "Sowing seeds in nursery beds.",
    "Transplant seedlings to main field.",
    "Ensure proper irrigation and fertilization.",
  ];

  List<String> descriptions = [
    "Clear the field of debris and weeds. Plow the soil to loosen it and break up clods. Level the field to ensure even water distribution.",
    "Choose certified seeds with high germination rates. Consider disease-resistant varieties suitable for your local climate and soil conditions.",
    "Prepare raised nursery beds with well-drained soil. Sow pre-soaked seeds evenly and maintain proper moisture levels.",
    "When seedlings reach 4-5 leaves stage, carefully uproot and transplant them to the main field in rows with proper spacing.",
    "Maintain appropriate water levels throughout growth stages. Apply fertilizers at recommended intervals and monitor for nutrient deficiencies.",
  ];

  List<bool> completed = [false, false, false, false, false];
  late AnimationController _animationController;
  late Animation<double> _animation;
  late Animation<double> _flowAnimation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 3000),
      vsync: this,
    )..repeat(reverse: false);

    _animation = CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeInOutCubic,
    );

    _flowAnimation = CurvedAnimation(
      parent: _animationController,
      curve: Curves.linear,
    );
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  void toggleCompletion(int index) {
    setState(() {
      completed[index] = !completed[index];
    });
  }

  void showStepDescription(int index) {
    showDialog(
      context: context,
      builder:
          (context) => AlertDialog(
            title: Text("Step ${index + 1}: ${steps[index]}"),
            content: Text(descriptions[index]),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(15),
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: Text("Close"),
                style: TextButton.styleFrom(foregroundColor: Color(0xFF2E7D32)),
              ),
              ElevatedButton(
                onPressed: () {
                  toggleCompletion(index);
                  Navigator.pop(context);
                },
                child: Text(
                  completed[index] ? "Mark as Incomplete" : "Mark as Complete",
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Color(0xFF2E7D32),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
              ),
            ],
          ),
    );
  }

  @override
  Widget build(BuildContext context) {
    // Calculate progress for the top bar
    int completedCount = completed.where((item) => item).length;
    double progress = completedCount / steps.length;

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        title: const Text(
          "Cultivation Roadmap",
          style: TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 24,
            color: Colors.white,
            shadows: [
              Shadow(
                blurRadius: 10.0,
                color: Colors.black45,
                offset: Offset(2.0, 2.0),
              ),
            ],
          ),
        ),
        flexibleSpace: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [Color(0xFF2E7D32), Color(0xFF1B5E20)],
            ),
          ),
        ),
        bottom: PreferredSize(
          preferredSize: Size.fromHeight(6.0),
          child: Container(
            height: 6.0,
            child: Stack(
              children: [
                Container(
                  width: double.infinity,
                  color: Colors.white.withOpacity(0.3),
                ),
                AnimatedContainer(
                  duration: Duration(milliseconds: 300),
                  width: MediaQuery.of(context).size.width * progress,
                  color: Colors.white,
                ),
              ],
            ),
          ),
        ),
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFFE8F5E9), Color(0xFFC8E6C9)],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: 24.0),
            child: Center(
              child: FadeTransition(
                opacity: _animation,
                child: _buildZigZagSteps(),
              ),
            ),
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          showDialog(
            context: context,
            builder:
                (context) => AlertDialog(
                  title: Text("Progress Summary"),
                  content: Text(
                    "You have completed $completedCount out of ${steps.length} steps.",
                  ),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: Text("OK"),
                    ),
                  ],
                ),
          );
        },
        label: Text("View Progress"),
        icon: Icon(Icons.analytics),
        backgroundColor: Color(0xFF2E7D32),
      ),
    );
  }

  Widget _buildZigZagSteps() {
    return SingleChildScrollView(
      child: Column(
        children: List.generate(steps.length * 2 - 1, (index) {
          if (index % 2 == 0) {
            // Step button
            final stepIndex = index ~/ 2;
            final isLeft = stepIndex % 2 == 0;

            return Row(
              mainAxisAlignment:
                  isLeft ? MainAxisAlignment.start : MainAxisAlignment.end,
              children: [
                if (!isLeft) Spacer(),
                InkWell(
                  onTap: () => showStepDescription(stepIndex),
                  child: Container(
                    width:
                        MediaQuery.of(context).size.width * 0.6, // Smaller box
                    margin: EdgeInsets.symmetric(vertical: 10),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(15),
                      boxShadow: [
                        BoxShadow(
                          color:
                              completed[stepIndex]
                                  ? Color(0xFF2E7D32).withOpacity(0.3)
                                  : Colors.black.withOpacity(0.1),
                          blurRadius: 8,
                          spreadRadius: 2,
                        ),
                      ],
                      border:
                          completed[stepIndex]
                              ? Border.all(color: Color(0xFF2E7D32), width: 2)
                              : null,
                    ),
                    child: Padding(
                      padding: EdgeInsets.all(12), // Smaller padding
                      child: Row(
                        children: [
                          Container(
                            width: 36, // Smaller circle
                            height: 36, // Smaller circle
                            decoration: BoxDecoration(
                              color:
                                  completed[stepIndex]
                                      ? Color(0xFF2E7D32)
                                      : Color(0xFFE8F5E9),
                              shape: BoxShape.circle,
                            ),
                            child: Center(
                              child: Text(
                                "${stepIndex + 1}",
                                style: TextStyle(
                                  color:
                                      completed[stepIndex]
                                          ? Colors.white
                                          : Color(0xFF2E7D32),
                                  fontWeight: FontWeight.bold,
                                  fontSize: 16, // Smaller font
                                ),
                              ),
                            ),
                          ),
                          SizedBox(width: 10),
                          Expanded(
                            child: Text(
                              steps[stepIndex],
                              style: TextStyle(
                                fontSize: 14, // Smaller font
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                          ),
                          Checkbox(
                            value: completed[stepIndex],
                            onChanged: (value) => toggleCompletion(stepIndex),
                            activeColor: Color(0xFF2E7D32),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
                if (isLeft) Spacer(),
              ],
            );
          } else {
            // Connecting line with dynamic color flow
            final fromIndex = index ~/ 2;
            final toIndex = fromIndex + 1;
            final isCompleted = completed[fromIndex] && completed[toIndex];

            return Container(
              height: 50,
              child: AnimatedBuilder(
                animation: _flowAnimation,
                builder: (context, child) {
                  return CustomPaint(
                    size: Size(double.infinity, 50),
                    painter: FlowingLinePainter(
                      isLeft: fromIndex % 2 == 0,
                      animationValue: _flowAnimation.value,
                      isCompleted: isCompleted,
                    ),
                  );
                },
              ),
            );
          }
        }),
      ),
    );
  }
}

// Custom painter for the flowing line effect
class FlowingLinePainter extends CustomPainter {
  final bool isLeft;
  final double animationValue;
  final bool isCompleted;

  FlowingLinePainter({
    required this.isLeft,
    required this.animationValue,
    required this.isCompleted,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final Paint linePaint =
        Paint()
          ..color =
              isCompleted
                  ? Color(0xFF2E7D32).withOpacity(0.5)
                  : Colors.grey.withOpacity(0.3)
          ..style = PaintingStyle.stroke
          ..strokeWidth = 2;

    final Paint flowPaint =
        Paint()
          ..color =
              isCompleted ? Color(0xFF2E7D32) : Colors.grey.withOpacity(0.7)
          ..style = PaintingStyle.stroke
          ..strokeWidth = 3;

    final Path path = Path();

    if (isLeft) {
      // Line from left to right
      path.moveTo(size.width * 0.3, 0);
      path.quadraticBezierTo(
        size.width * 0.5,
        size.height * 0.5,
        size.width * 0.7,
        size.height,
      );
    } else {
      // Line from right to left
      path.moveTo(size.width * 0.7, 0);
      path.quadraticBezierTo(
        size.width * 0.5,
        size.height * 0.5,
        size.width * 0.3,
        size.height,
      );
    }

    // Draw the base line
    canvas.drawPath(path, linePaint);

    // Draw the flowing effect
    final PathMetrics pathMetrics = path.computeMetrics();
    for (PathMetric pathMetric in pathMetrics) {
      final double pathLength = pathMetric.length;

      // Calculate start and end for the flowing segment
      final double start = (animationValue - 0.2) * pathLength;
      final double end = animationValue * pathLength;

      if (start > 0 && start < pathLength) {
        final Path extractPath = pathMetric.extractPath(
          start < 0 ? 0 : start,
          end > pathLength ? pathLength : end,
        );
        canvas.drawPath(extractPath, flowPaint);
      }

      // Draw a small circle at the flow point
      if (end > 0 && end < pathLength) {
        final Tangent? tangent = pathMetric.getTangentForOffset(end);
        if (tangent != null) {
          canvas.drawCircle(
            tangent.position,
            4,
            Paint()..color = isCompleted ? Color(0xFF2E7D32) : Colors.grey,
          );
        }
      }
    }

    // Draw arrow at the end
    final Offset arrowPosition =
        isLeft
            ? Offset(size.width * 0.7, size.height)
            : Offset(size.width * 0.3, size.height);

    canvas.drawCircle(
      arrowPosition,
      6,
      Paint()
        ..color =
            isCompleted ? Color(0xFF2E7D32) : Colors.grey.withOpacity(0.7),
    );
  }

  @override
  bool shouldRepaint(FlowingLinePainter oldDelegate) {
    return oldDelegate.animationValue != animationValue ||
        oldDelegate.isCompleted != isCompleted;
  }
}
