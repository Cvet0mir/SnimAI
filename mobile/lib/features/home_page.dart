import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../core/widgets/app_scaffold.dart';
import '../core/widgets/navigation_menu.dart';
import '../core/widgets/primary_button.dart';

import '../core/services/auth/auth_service.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  //  Testing session ------------------------------------
  final String _lastSessionTitle = "Linear Algebra Notes";
  final DateTime _lastSessionCreated =
      DateTime.now().subtract(const Duration(hours: 5));

  final DateTime _lastActiveDate =
      DateTime.now().subtract(const Duration(days: 1));

  // ------------------------------------------------------

  String _getGreeting() {
    final hour = DateTime.now().hour;

    if (hour < 12) return "Добро утро";
    if (hour < 18) return "Добър ден";
    return "Добър вечер";
  }

  String _getFormattedDate() {
    return DateFormat("EEEE, MMMM d, y", "bg").format(DateTime.now());
  }

  String _getDailyMotivation() {
    final motivations = [
      "Стремете се към прогрес, не към съвършенство.",
      "Пропускаш 100% от възможностите, които не предприемаш.",
      "Ако не правиш грешки, значи не се опитваш истински.",
      "Мотивацията почти винаги е по-важна от простия талант.",
      "Just do it™.",
      "Тайната да излезеш начело е да започнеш.",
      "Разликата между цел и мечта е крайният срок.",
      "Нищо велико не е постигнато без ентусиазъм"
    ];

    final dayOfYear = int.parse(DateFormat("D").format(DateTime.now()));
    return motivations[dayOfYear % motivations.length];
  }

  String _name = '';
  // the way for its increment will be rethought
  int _streak = 0;

  @override
  void initState() {
    super.initState();
    _loadProfile();
  }

  Future<void> _loadProfile() async {
    final user = await AuthService().getProfile();
    setState(() {
      _name = user.name;
      _streak = user.currentStreak;
    });
  }

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'Начало',
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                "${_getGreeting()}, $_name 👋",
                style: Theme.of(context).textTheme.headlineSmall,
              ),

              const SizedBox(height: 6),

              Text(
                _getFormattedDate(),
                style: Theme.of(context).textTheme.bodyMedium,
              ),

              const SizedBox(height: 20),

              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(16),
                  color: Colors.blue.withOpacity(0.08),
                ),
                child: Text(
                  _getDailyMotivation(),
                  style: Theme.of(context).textTheme.bodyLarge,
                ),
              ),

              const SizedBox(height: 30),

              PrimaryButton(
                height: 55,
                text: 'Започнете нова сесия',
                onPressed: () {},
                icon: Icon(Icons.add),
              ),

              const SizedBox(height: 30),

              Text(
                "Last Session",
                style: Theme.of(context).textTheme.titleMedium,
              ),

              const SizedBox(height: 10),

              Card(
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                child: ListTile(
                  title: Text(_lastSessionTitle),
                  subtitle: Text(
                    "Created ${DateFormat("MMM d, HH:mm").format(_lastSessionCreated)}",
                  ),
                  trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                  onTap: () {},
                ),
              ),

              const SizedBox(height: 30),

              Text(
                "Твоята серия",
                style: Theme.of(context).textTheme.titleMedium,
              ),

              const SizedBox(height: 10),

              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(16),
                  color: Colors.orange.withOpacity(0.1),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.local_fire_department,
                        color: Colors.orange),
                    const SizedBox(width: 12),
                    Text(
                      "$_streak дни подред",
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
