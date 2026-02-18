import 'package:flutter/material.dart';

import '../../../core/widgets/app_scaffold.dart';
import '../../../core/widgets/loading_indicator.dart';
import '../../../core/widgets/primary_button.dart';
import '../../../core/utils/helpers.dart';
import '../../../core/utils/validators.dart';
import '../core/services/auth/auth_service.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _authService = AuthService();

  bool _isLoading = false;

  Future<void> _login() async {
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    if (!Validators.isValidEmail(email)) {
      Helpers.showSnackBar(context, "Невалиден имейл");
      return;
    }

    if (!Validators.isValidPassword(password)) {
      Helpers.showSnackBar(context, "Паролата трябва да е поне 6 символа дълга");
      return;
    }

    setState(() => _isLoading = true);

    try {
      await _authService.login(email, password);

      if (!mounted) return;

      Navigator.pushReplacementNamed(context, '/home');
    } catch (e) {
      Helpers.showSnackBar(context, e.toString());
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'Влизане в профил',
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: _isLoading
            ? const LoadingIndicator()
            : Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  TextField(
                    controller: _emailController,
                    decoration: const InputDecoration(labelText: 'Имейл:'),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: _passwordController,
                    obscureText: true,
                    decoration: const InputDecoration(labelText: 'Парола:'),
                  ),
                  const SizedBox(height: 24),
                  PrimaryButton(
                    text: 'Влез',
                    onPressed: _login,
                  ),
                  const SizedBox(height: 12),
                  TextButton(
                    onPressed: () {
                      Navigator.pushNamed(context, '/register');
                    },
                    child: const Text("Нямаш акаунт? Регистрирай се"),
                  ),
                ],
              ),
      ),
    );
  }
}
