import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../../config/app_constants.dart';
import '../api/endpoints.dart';
import '../api/exceptions.dart';

class AuthService {
  final String baseUrl = AppConstants.baseUrl;

  Future<void> login(String email,String password) async {
    final url = Uri.parse('$baseUrl${ApiEndpoints.login}');

    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'password': password,
      }),
    );

    if (response.statusCode != 200) {
    final decoded = jsonDecode(response.body);
    final detail = decoded['detail'];

    String errorMessage;

    if (detail is String) {
      errorMessage = detail;
    } else if (detail is List) {
      errorMessage = detail.map((e) => e['msg']).join(', ');
    } else {
      errorMessage = 'Грешен имейл или парола';
    }

    throw ApiException(
      errorMessage,
      statusCode: response.statusCode,
    );
  }


    final data = jsonDecode(response.body);

    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(AppConstants.accessTokenKey, data['access_token']);
    await prefs.setString(AppConstants.refreshTokenKey, data['refresh_token']);
  }

  Future<void> register(String email, String name, String password) async {
    final url = Uri.parse('$baseUrl${ApiEndpoints.register}');

    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'name': name,
        'password': password,
      }),
    );

    if (response.statusCode != 201) {
      throw ApiException(
        jsonDecode(response.body)['detail'] ?? 'Неуспешна регистрация. Моля, опитайте отново',
        statusCode: response.statusCode,
      );
    }
  }

  Future<bool> isLoggedIn() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.containsKey(AppConstants.accessTokenKey);
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(AppConstants.accessTokenKey);
    await prefs.remove(AppConstants.refreshTokenKey);
  }
}
