import 'package:flutter/material.dart';

import '../core/widgets/app_scaffold.dart';
import '../core/widgets/navigation_menu.dart';
import '../core/widgets/loading_indicator.dart';

import '../core/services/auth/auth_service.dart';
import '../core/services/sessions/session_service.dart';
import '../core/models/user_model.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  final AuthService _authService = AuthService();
  late Future<UserModel> _profileFuture;

  bool _isLoggingOut = false;
  int _selectedIndex = 2;

  @override
  void initState() {
    super.initState();
    _profileFuture = _authService.getProfile();
  }

  Future<void> _handleLogout() async {
    setState(() {
      _isLoggingOut = true;
    });

    await _authService.logout();

    if (!mounted) return;

    Navigator.pushReplacementNamed(context, '/login');

    Future.delayed(Duration.zero, () {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Успешно излязохте от профила си"),
          duration: Duration(seconds: 3),
        ),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'Профил',
      body: _isLoggingOut
          ? const LoadingIndicator()
          : FutureBuilder<UserModel>(
              future: _profileFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState ==
                    ConnectionState.waiting) {
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

                final user = snapshot.data!;

                return Padding(
                  padding: const EdgeInsets.symmetric(
                      horizontal: 20, vertical: 24),
                  child: Column(
                    children: [
                      CircleAvatar(
                        radius: 50,
                        backgroundColor: Colors.grey.shade300,
                        child: const Icon(
                          Icons.person,
                          size: 50,
                          color: Colors.white,
                        ),
                      ),

                      const SizedBox(height: 16),

                      Text(
                        user.name,
                        style: const TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.bold,
                        ),
                      ),

                      const SizedBox(height: 4),

                      Text(
                        user.email,
                        style: TextStyle(
                          fontSize: 16,
                          color: Color.fromARGB(255, 117, 117, 117),
                        ),
                      ),
                      const SizedBox(height: 12),

                      FutureBuilder<int>(
                        future: SessionService().getSessionsCount(),
                        builder: (context, snapshot) {
                          if (snapshot.connectionState == ConnectionState.waiting) {
                            return const SizedBox(
                              height: 20,
                              width: 20,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            );
                          }

                          if (snapshot.hasError) {
                            return const Text(
                              'Грешка при зареждане на сесиите',
                              style: TextStyle(color: Color.fromARGB(255, 117, 117, 117)),
                            );
                          }

                          final count = snapshot.data ?? 0;

                          return Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 16,
                              vertical: 8,
                            ),
                            decoration: BoxDecoration(
                              color: Colors.blue.shade50,
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Text(
                              "Създадени сесии: $count",
                              style: const TextStyle(
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          );
                        },
                      ),
                      const SizedBox(height: 32),

                      Card(
                        shape: RoundedRectangleBorder(
                          borderRadius:
                              BorderRadius.circular(12),
                        ),
                        child: Column(
                          children: const [
                            ListTile(
                              leading: Icon(Icons.settings),
                              title: Text("Настройки"),
                              trailing: Icon(
                                  Icons.arrow_forward_ios,
                                  size: 16),
                            ),
                            Divider(height: 1),
                            ListTile(
                              leading: Icon(Icons.lock),
                              title: Text("Промени парола"),
                              trailing: Icon(
                                  Icons.arrow_forward_ios,
                                  size: 16),
                            ),
                          ],
                        ),
                      ),

                      const Spacer(),

                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton(
                          onPressed: _handleLogout,
                          style:
                              ElevatedButton.styleFrom(
                            backgroundColor: Colors.red,
                            padding:
                                const EdgeInsets.symmetric(
                                    vertical: 14),
                            shape:
                                RoundedRectangleBorder(
                              borderRadius:
                                  BorderRadius.circular(
                                      12),
                            ),
                          ),
                          child: const Text(
                            "Изход",
                            style:
                                TextStyle(fontSize: 16),
                          ),
                        ),
                      ),
                    ],
                  ),
                );
              },
            ),
      bottomNavigationBar:
          CustomBottomMenu(currentIndex: _selectedIndex),
    );
  }
}