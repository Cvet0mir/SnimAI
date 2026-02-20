import 'package:flutter/material.dart';

import '../../features/home_page.dart';
import '../../features/sessions_page.dart';
import '../../features/profile_page.dart';

class CustomBottomMenu extends StatelessWidget {
  final int currentIndex;

  const CustomBottomMenu({super.key, required this.currentIndex});

  void _navigate(BuildContext context, int index) {
    if (index == currentIndex) return;

    Widget page;

    switch (index) {
      case 0:
        page = const HomePage();
        break;
      case 1:
        page = const SessionsPage();
        break;
      case 2:
        page = const ProfilePage();
        break;
      default:
        page = const HomePage();
    }

    Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => page));
  }

  @override
  Widget build(BuildContext context) {
    return BottomNavigationBar(
      backgroundColor: Colors.orange,
      unselectedItemColor: Colors.white70,
      currentIndex: currentIndex,
      onTap: (index) => _navigate(context, index),
      items: const [
        BottomNavigationBarItem(icon: Icon(Icons.home), label: "Начало"),
        BottomNavigationBarItem(
          icon: Icon(Icons.image_rounded),
          label: "Качване на снимки",
        ),
        BottomNavigationBarItem(icon: Icon(Icons.person), label: "Профил"),
      ],
    );
  }
}
