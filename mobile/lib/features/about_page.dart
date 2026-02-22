import 'package:flutter/material.dart';

import '../core/widgets/app_scaffold.dart';

class AboutPage extends StatelessWidget {
  const AboutPage({super.key});

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: "За нас",
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const SizedBox(height: 20),

            Image.asset(
              'assets/logo.png',
              height: 198,
            ),

            const SizedBox(height: 2),

            Text(
              "Версия 1.0.0",
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey.shade600,
              ),
            ),

            const SizedBox(height: 21),

            const Text(
              "SnimAI е модерно приложение за учене и продуктивност, създадено да ви помага да проследявате своeто обучение, "
              "да организирате бележките си и да подобрявате своя работен процес.\n\n"
              "Изградено с Flutter и FastAPI, приложението се фокусира върху изчистен дизайн, "
              "опростеност и висока производителност.",
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 16,
                height: 1.5,
              ),
            ),

            const Spacer(),

            const Divider(),

            const SizedBox(height: 10),

            const Text(
              "© 2026 SnimAI\n"
              "Лицензирано под GNU General Public License v3.0 (GPL-3.0).",
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 13,
                color: Colors.grey,
              ),
            ),

            const SizedBox(height: 10),
          ],
        ),
      ),
    );
  }
}