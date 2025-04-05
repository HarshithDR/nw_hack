import 'package:flutter/material.dart';
import 'package:frontend_wildhacks/Home/home.dart';

void main() => runApp(MyAgri());

class MyAgri extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: AgriHome(),
      theme: ThemeData(useMaterial3: true),
    );
  }
}
