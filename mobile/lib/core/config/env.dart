import 'package:flutter_dotenv/flutter_dotenv.dart';

class Env {
  static final String environmentMode = dotenv.env['ENV'] ?? 'dev';
}
