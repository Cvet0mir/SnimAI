import 'package:flutter/material.dart';

import '../core/widgets/app_scaffold.dart';
import '../core/widgets/navigation_menu.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'Home Page',
      body: const Center(child: Text("Home Page")),

      bottomNavigationBar: CustomBottomMenu(currentIndex: _selectedIndex),
    );
  }
}
