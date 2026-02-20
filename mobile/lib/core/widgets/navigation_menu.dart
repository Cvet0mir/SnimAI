import 'package:flutter/material.dart';

class CustomBottomMenu extends StatelessWidget {
  final int currentIndex;
  final Function(int) onTap;

  const CustomBottomMenu({
    super.key,
    required this.currentIndex,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return BottomNavigationBar(
      backgroundColor: Colors.orange,
      unselectedItemColor: Colors.white70,
      currentIndex: currentIndex,
      onTap: onTap,
      items: const [
        BottomNavigationBarItem(icon: Icon(Icons.home), label: "Начало"),
        BottomNavigationBarItem(
          icon: Icon(Icons.photo_size_select_actual_sharp),
          label: "Качване на снимки",
        ),
        BottomNavigationBarItem(icon: Icon(Icons.person), label: "Профил"),
      ],
    );
  }
}
