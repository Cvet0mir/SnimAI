import 'package:flutter/material.dart';

import 'profile_page.dart';
import 'home_page.dart';
import 'sessions_page.dart';
import 'about_page.dart';
import '../core/widgets/navigation_menu.dart';

class MainNavigationPage extends StatefulWidget {
  const MainNavigationPage({super.key});

  @override
  State<MainNavigationPage> createState() => _MainNavigationPageState();
}

class _MainNavigationPageState extends State<MainNavigationPage> {
  int _selectedIndex = 0;

  final List<Widget> _pages = const [
    HomePage(),
    SessionsPage(),
    ProfilePage(),
    AboutPage(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_selectedIndex],
      bottomNavigationBar: CustomBottomMenu(
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
      ),
    );
  }
}
