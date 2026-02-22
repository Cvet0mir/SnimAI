import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../core/services/api/exceptions.dart';
import '../core/services/api/endpoints.dart';
import '../core/config/app_constants.dart';
import '../core/widgets/app_scaffold.dart';

class CreateSessionPage extends StatefulWidget {
  const CreateSessionPage({super.key});

  @override
  State<CreateSessionPage> createState() => _CreateSessionPageState();
}

class _CreateSessionPageState extends State<CreateSessionPage> {
  final TextEditingController _sessionNameController =
      TextEditingController();

  final List<File> _selectedImages = [];
  final ImagePicker _picker = ImagePicker();

  bool _isLoading = false;
  Future<void> _pickFromGallery() async {
    final List<XFile> images = await _picker.pickMultiImage();

    if (images.isNotEmpty) {
      setState(() {
        _selectedImages.addAll(images.map((x) => File(x.path)));
      });
    }
  }
  Future<void> _takePhoto() async {
    final XFile? image =
        await _picker.pickImage(source: ImageSource.camera);

    if (image != null) {
      setState(() {
        _selectedImages.add(File(image.path));
      });
    }
  }

  Future<void> _createSession() async {
    if (_sessionNameController.text.trim().isEmpty) return;

    setState(() => _isLoading = true);

    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString(AppConstants.accessTokenKey);

      if (token == null) throw ApiException("Потребителят не е удостоверен");

      final sessionResponse = await http.post(
        Uri.parse('${AppConstants.baseUrl}${ApiEndpoints.createSession}'),
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token",
        },
        body: jsonEncode({
          "name": _sessionNameController.text.trim(),
          "status": "PENDING",
        }),
      );

      if (sessionResponse.statusCode != 201) {
        throw ApiException("Грешка при създаване на сесия: ${sessionResponse.body}");
      }

      final sessionData = jsonDecode(sessionResponse.body);
      final sessionId = sessionData["id"];

      for (final image in _selectedImages) {
        final request = http.MultipartRequest(
          "POST",
          Uri.parse('${AppConstants.baseUrl}${ApiEndpoints.addNoteToSession(sessionId)}'),
        );

        request.headers["Authorization"] = "Bearer $token";

        request.files.add(
          await http.MultipartFile.fromPath("image", image.path),
        );

        final response = await request.send();

        if (response.statusCode != 201) {
          throw ApiException("Грешка при качване на изображение (код: ${response.statusCode})");
        }
      }

      if (!mounted) return;
      Navigator.pop(context, true);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.toString())),
      );
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'Нова сесия',
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _sessionNameController,
              decoration: const InputDecoration(
                labelText: "Име на сесията",
              ),
            ),
            const SizedBox(height: 20),

            ElevatedButton.icon(
              onPressed: _pickFromGallery,
              icon: const Icon(Icons.photo_library),
              label: const Text("Избери от галерията"),
            ),

            const SizedBox(height: 10),

            ElevatedButton.icon(
              onPressed: _takePhoto,
              icon: const Icon(Icons.camera_alt),
              label: const Text("Направи снимка"),
            ),

            const SizedBox(height: 20),

            Expanded(
              child: GridView.builder(
                itemCount: _selectedImages.length,
                gridDelegate:
                    const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 3,
                  crossAxisSpacing: 6,
                  mainAxisSpacing: 6,
                ),
                itemBuilder: (context, index) {
                  return Image.file(
                    _selectedImages[index],
                    fit: BoxFit.cover,
                  );
                },
              ),
            ),

            const SizedBox(height: 10),

            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _selectedImages.isNotEmpty &&
                        !_isLoading
                    ? _createSession
                    : null,
                child: _isLoading
                    ? const CircularProgressIndicator()
                    : const Text("Създай сесия"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
