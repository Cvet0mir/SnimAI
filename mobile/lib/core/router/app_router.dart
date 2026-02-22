import 'package:flutter/material.dart';

import '../../features/login_page.dart';
import '../../features/register_page.dart';
import '../../features/splash_screen.dart';
import '../../features/main_nav_page.dart';

class AppRouter {
  static Map<String, Widget Function(BuildContext)> routes = {
    '/': (context) => const SplashScreen(),
    '/login': (context) => const LoginPage(),
    '/register': (context) => const RegisterPage(),
    '/home': (context) => const MainNavigationPage(),
  };
}
