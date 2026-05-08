import 'package:flutter/material.dart';

void main() {
  runApp(EduAccessAI());
}

class EduAccessAI extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EduAccess AI',
      home: Scaffold(
        appBar: AppBar(
          title: Text('EduAccess AI'),
        ),
        body: Center(
          child: Text('Inclusive Learning Platform'),
        ),
      ),
    );
  }
}
