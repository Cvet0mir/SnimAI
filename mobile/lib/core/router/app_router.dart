import 'package:flutter/material.dart';

class AppRouter {
  static Map<String, Widget Function(BuildContext)> routes = {
    '/': (context) => const PlaceholderPage(
        title: 'Mock Home',
      ),
  };
}

class PlaceholderPage extends StatelessWidget {
  final String title;
  const PlaceholderPage({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: const Center(child: Text('Test text')),
    );
  }
}
