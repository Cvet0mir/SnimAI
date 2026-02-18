class ApiEndpoints {
  static const String _base = '/api/v1';

  static const String login = '$_base/auth/login';
  static const String register = '$_base/auth/register';
  static const String refresh = '$_base/auth/refresh';

  static const String profile = '$_base/auth/me';
  static const String updateProfile = '$_base/auth/me';
  static const String deleteProfile = '$_base/auth/me';

  static const String createSession = '$_base/sessions';
  static const String getSessions = '$_base/sessions';
  static String getSessionById(int sessionId) => '$_base/sessions/$sessionId';
  static String deleteSession(int sessionId) => '$_base/sessions/$sessionId';

  static const String addNote = '$_base/notes';
  static const String getNotes = '$_base/notes';
  static String getNoteById(int noteId) => '$_base/notes/$noteId';
  static String updateNote(int noteId) => '$_base/notes/$noteId';
  static String deleteNote(int noteId) => '$_base/notes/$noteId';

  static String startProcessing(int sessionId) => '$_base/processing/start/$sessionId';
  static String getProcessingStatus(int sessionId) => '$_base/processing/status/$sessionId';
  static String processingResult(int sessionId) => '$_base/processing/result/$sessionId';
}
