import 'package:flutter/material.dart';

import '../core/widgets/app_scaffold.dart';
import '../core/widgets/navigation_menu.dart';

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    int _selectedIndex = 2;

    return AppScaffold(
      title: 'Профил',
      body: const Center(child: Text("Профил")),
      bottomNavigationBar: CustomBottomMenu(currentIndex: _selectedIndex),
    );
  }
}
