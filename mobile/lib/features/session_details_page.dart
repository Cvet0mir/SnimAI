import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../core/config/app_constants.dart';
import '../core/services/api/endpoints.dart';
import '../core/widgets/app_scaffold.dart';

class SessionDetailsPage extends StatefulWidget {
  final int sessionId;

  const SessionDetailsPage({super.key, required this.sessionId});

  @override
  State<SessionDetailsPage> createState() => _SessionDetailsPageState();
}

class _SessionDetailsPageState extends State<SessionDetailsPage> {
  Map<String, dynamic>? session;
  List<dynamic> notes = [];
  Map<String, dynamic>? summary;
  List<dynamic> quizzes = [];

  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadAllData();
  }

  Future<Map<String, String>> _authHeaders() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString(AppConstants.accessTokenKey);

    return {
      "Content-Type": "application/json",
      "Authorization": "Bearer $token",
    };
  }

  Future<void> _loadAllData() async {
    try {
      final headers = await _authHeaders();

      final baseUrl = AppConstants.baseUrl;

      final sessionRes = await http.get(
        Uri.parse('$baseUrl${ApiEndpoints.getSessionById(widget.sessionId)}'),
        headers: headers,
      );

      final notesRes = await http.get(
        Uri.parse('$baseUrl${ApiEndpoints.getSessionNotes(widget.sessionId)}'),
        headers: headers,
      );

      final summaryRes = await http.get(
        Uri.parse('$baseUrl${ApiEndpoints.getSessionSummary(widget.sessionId)}'),
        headers: headers,
      );

      final quizzesRes = await http.get(
        Uri.parse('$baseUrl${ApiEndpoints.getSessionQuizzes(widget.sessionId)}'),
        headers: headers,
      );

      setState(() {
        session = jsonDecode(sessionRes.body);
        notes = jsonDecode(notesRes.body);
        summary = summaryRes.statusCode == 200
            ? jsonDecode(summaryRes.body)
            : null;
        quizzes = jsonDecode(quizzesRes.body);
        isLoading = false;
      });
    } catch (e) {
      setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return AppScaffold(
      title: session?["name"],
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [

            const Text(
              "Бележки",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),

            if (notes.isEmpty)
              const Text("Няма качени бележки.")
            else
              Column(
                children: notes.map((note) {
                  return Card(
                    child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          if (note["image_path"] != null)
                            ClipRRect(
                              borderRadius: BorderRadius.circular(8),
                              child: Image.network(
                                '${AppConstants.baseUrl}${note["image_path"]}',
                                fit: BoxFit.cover,
                                errorBuilder: (context, error, stackTrace) {
                                  return const Text("Грешка при зареждане на изображението");
                                },
                              ),
                            ),
                        ],
                      ),
                    ),
                  );
                }).toList(),
              ),

            const SizedBox(height: 24),

            const Text(
              "Обобщение",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),

            summary == null
                ? const Text("Няма обобщение.")
                : Text(summary!["content"] ?? ""),

            const SizedBox(height: 24),

            const Text(
              "Тестове",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),

            if (quizzes.isEmpty)
              const Text("Няма тестове.")
            else
              Column(
                children: quizzes.map((quiz) {
                  final questions = quiz["questions"] as List<dynamic>? ?? [];

                  return Column(
                    children: questions.map((q) {
                      return Card(
                        child: Padding(
                          padding: const EdgeInsets.all(12),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                q["question"] ?? "",
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 6),
                              Text("Отговор: ${q["correct_answer"] ?? ""}"),
                            ],
                          ),
                        ),
                      );
                    }).toList(),
                  );
                }).toList(),
              ),
          ],
        ),
      ),
    );
  }
}