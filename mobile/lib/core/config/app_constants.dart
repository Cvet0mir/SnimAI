import 'package:flutter_dotenv/flutter_dotenv.dart';

class AppConstants {
  static final String baseUrl = dotenv.env['API_BASE_URL'] ?? 'http://localhost:8000';

  static const String accessTokenKey = 'access_token';
  static const String refreshTokenKey = 'refresh_token';
}
