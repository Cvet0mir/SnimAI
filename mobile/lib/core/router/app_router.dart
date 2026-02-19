import 'package:flutter/material.dart';

import '../../features/login_page.dart';
import '../../features/register_page.dart';
import '../../features/splash_screen.dart';

class AppRouter {
  static Map<String, Widget Function(BuildContext)> routes = {
    '/': (context) => const SplashScreen(),
    '/login': (context) => const LoginPage(),
    '/register': (context) => const RegisterPage(),
    '/home': (context) => const PlaceholderPage(title: 'Home'),
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
