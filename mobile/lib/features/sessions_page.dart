import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../core/widgets/app_scaffold.dart';
import '../core/widgets/loading_indicator.dart';
import '../core/services/sessions/session_service.dart';
import '../features/session_details_page.dart';

class SessionsPage extends StatefulWidget {
  const SessionsPage({super.key});

  @override
  State<SessionsPage> createState() => _SessionsPageState();
}

class _SessionsPageState extends State<SessionsPage> {
  final SessionService _sessionService = SessionService();
  late Future<List<dynamic>> _sessionsFuture;

  @override
  void initState() {
    super.initState();
    _sessionsFuture = _sessionService.getSessions();
  }

  String _formatDate(String dateString) {
    final date = DateTime.parse(dateString);
    return DateFormat('dd.MM.yyyy – HH:mm').format(date);
  }

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'Сесии',
      body: FutureBuilder<List<dynamic>>(
        future: _sessionsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const LoadingIndicator();
          }

          if (snapshot.hasError) {
            return Center(
              child: Text(
                snapshot.error.toString(),
                style: const TextStyle(color: Colors.red),
              ),
            );
          }

          final sessions = snapshot.data ?? [];

          if (sessions.isEmpty) {
            return const Center(
              child: Text("Все още не сте създали сесия. Започнете да качвате още сега!"),
            );
          }

          return ListView.builder(
            itemCount: sessions.length,
            itemBuilder: (context, index) {
              final session = sessions[index];

              return Card(
                child: ListTile(
                  title: Text(session["name"]),
                  subtitle: Text(_formatDate(session["created_at"])),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => SessionDetailsPage(
                          sessionId: session["id"],
                        ),
                      ),
                    );
                  },
                ),
              );
            },
          );
        },
      ),

      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          final result = await Navigator.pushNamed(
            context,
            '/create-session',
          );

          if (result == true) {
            setState(() {
              _sessionsFuture =
                  _sessionService.getSessions();
            });
          }
        },
        child: const Icon(Icons.add),
      ),
      floatingActionButtonLocation:
          FloatingActionButtonLocation.endFloat,
    );
  }
}