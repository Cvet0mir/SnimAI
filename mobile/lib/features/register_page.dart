import 'package:flutter/material.dart';

import '../../../core/widgets/app_scaffold.dart';
import '../../../core/widgets/loading_indicator.dart';
import '../../../core/widgets/primary_button.dart';
import '../../../core/utils/helpers.dart';
import '../../../core/utils/validators.dart';
import '../core/services/auth/auth_service.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _emailController = TextEditingController();
  final _nameController = TextEditingController();
  final _passwordController = TextEditingController();
  final _authService = AuthService();

  bool _isLoading = false;

  Future<void> _register() async {
    final email = _emailController.text.trim();
    final name = _nameController.text.trim();
    final password = _passwordController.text.trim();

    if (!Validators.isValidEmail(email)) {
      Helpers.showSnackBar(context, "Грешен имейл или парола");
      return;
    }

    if (!Validators.isValidPassword(password)) {
      Helpers.showSnackBar(context, "Паролата трябва да е поне 6 символа дълга");
      return;
    }

    setState(() => _isLoading = true);

    try {
      await _authService.register(email, name, password);

      if (!mounted) return;

      Helpers.showSnackBar(context, "Успешна регистрация! Моля, влезте в новия си профил сега");
      Navigator.pushReplacementNamed(context, '/login');
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
      title: 'Регистрация',
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
                    controller: _nameController,
                    obscureText: true,
                    decoration: const InputDecoration(labelText: 'Име:'),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: _passwordController,
                    obscureText: true,
                    decoration: const InputDecoration(labelText: 'Парола:'),
                  ),
                  const SizedBox(height: 24),
                  PrimaryButton(
                    text: 'Регистрирай се',
                    onPressed: _register,
                  ),
                  const SizedBox(height: 12),
                  TextButton(
                    onPressed: () {
                      Navigator.pop(context);
                    },
                    child: const Text("Вече имаш акаунт? Влез в акаунта си"),
                  ),
                ],
              ),
      ),
    );
  }
}
