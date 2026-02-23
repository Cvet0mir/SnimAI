import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../core/widgets/app_scaffold.dart';
import '../core/widgets/primary_button.dart';

import '../core/services/auth/auth_service.dart';
import '../core/services/sessions/session_service.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final SessionService _sessionService = SessionService();

  Map<String, dynamic>? _lastSession;
  bool _isLoadingSession = true;

  String _name = '';
  int _streak = 0;

  @override
  void initState() {
    super.initState();
    _loadProfile();
    _loadLastSession();
  }

  Future<void> _loadProfile() async {
    final user = await AuthService().getProfile();
    setState(() {
      _name = user.name;
      _streak = user.currentStreak;
    });
  }

  Future<void> _loadLastSession() async {
    try {
      final sessions = await _sessionService.getSessions();

      if (sessions.isNotEmpty) {
        // Sort sessions by created_at descending (newest first)
        sessions.sort((a, b) =>
            DateTime.parse(b["created_at"])
                .compareTo(DateTime.parse(a["created_at"])));

        setState(() {
          _lastSession = sessions.first;
          _isLoadingSession = false;
        });
      } else {
        setState(() {
          _lastSession = null;
          _isLoadingSession = false;
        });
      }
    } catch (e) {
      setState(() {
        _isLoadingSession = false;
      });
    }
  }

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
                onPressed: () async {
                  final result =
                      await Navigator.pushNamed(context, '/create-session');

                  if (result == true) {
                    _loadLastSession();
                  }
                },
                icon: const Icon(Icons.add),
              ),

              const SizedBox(height: 30),

              Text(
                "Last Session",
                style: Theme.of(context).textTheme.titleMedium,
              ),

              const SizedBox(height: 10),

              if (_isLoadingSession)
                const Center(child: CircularProgressIndicator())
              else if (_lastSession == null)
                const Text("Все още няма създадени сесии.")
              else
                Card(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: ListTile(
                    title: Text(_lastSession!["name"]),
                    subtitle: Text(
                      "Created ${DateFormat("MMM d, HH:mm").format(
                        DateTime.parse(_lastSession!["created_at"]),
                      )}",
                    ),
                    trailing:
                        const Icon(Icons.arrow_forward_ios, size: 16),
                    onTap: () {
                      Navigator.pushNamed(
                        context,
                        '/session-details',
                        arguments: _lastSession!["id"],
                      );
                    },
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