import 'package:flutter/material.dart';
import 'package:frontend_wildhacks/pageviewer/pageviewer.dart';

void main() => runApp(MyAgri());

class MyAgri extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: PageViewer(),
      theme: ThemeData(useMaterial3: true),
    );
  }
}
