import 'dart:ffi';

import 'package:flutter/material.dart';

class PrimaryButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final double? height;
  final Icon? icon;

  const PrimaryButton({
    super.key,
    required this.text,
    required this.onPressed,
    this.height,
    this.icon
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      height: height,
      child: ElevatedButton.icon(
          onPressed: onPressed,
          label: Text(text),
          icon: icon,
        )
    );
  }
}

