class Validators {
  static bool isValidEmail(String value) {
    return value.contains('@');
  }

  static bool isValidPassword(String value) {
    return value.length >= 6;
  }
}
