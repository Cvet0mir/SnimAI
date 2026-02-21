class UserModel {
  final int id;
  final String email;
  final String name;
  final int currentStreak;

  UserModel({
    required this.id,
    required this.email,
    required this.name,
    required this.currentStreak,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      email: json['email'],
      name: json['name'],
      currentStreak: json['current_streak'] ?? 0,
    );
  }
}