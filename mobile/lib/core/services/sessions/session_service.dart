import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../../config/app_constants.dart';
import '../api/endpoints.dart';
import '../api/exceptions.dart';

class SessionService {
  final String baseUrl = AppConstants.baseUrl;

  Future<Map<String, String>> _authHeaders() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString(AppConstants.accessTokenKey);

    if (token == null) {
      throw ApiException("Потребителят не е удостоверен");
    }

    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };
  }

  Future<List<dynamic>> getSessions() async {
    final url = Uri.parse('$baseUrl${ApiEndpoints.getSessions}');
    final headers = await _authHeaders();

    final response = await http.get(url, headers: headers);

    if (response.statusCode != 200) {
      print(response.statusCode);
      throw ApiException(
        "Неуспешно зареждане на сесиите",
        statusCode: response.statusCode,
      );
    }

    if (response.body.isEmpty) return [];

    final decoded = jsonDecode(response.body);

    if (decoded is List) {
      return decoded;
    } else {
      throw ApiException("Непознат формат на данните от сървъра");
    }
  }

  Future<int> getSessionsCount() async {
    final sessions = await getSessions();
    return sessions.length;
  }
}
