import 'package:flutter/material.dart';

import '../core/widgets/app_scaffold.dart';
import '../core/widgets/navigation_menu.dart';

class SessionsPage extends StatelessWidget {
  const SessionsPage({super.key});

  @override
  Widget build(BuildContext context) {
    int _selectedIndex = 1;

    return AppScaffold(
      title: 'Sessions Page',
      body: const Center(child: Text("Sessions Page")),
      bottomNavigationBar: CustomBottomMenu(currentIndex: _selectedIndex),
    );
  }
}
