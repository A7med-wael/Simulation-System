import 'package:flutter/material.dart';

enum DialogType { Success, Failure }

class CustomDialog {
  static void showCustomDialog({
    required BuildContext context,
    required String title,
    required String description,
    required DialogType dialogType,
    String? btnOkText,
    String? btnCancelText,
    Function? onOkPressed,
    Function? onCancelPressed,
  }) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return Dialog(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16.0),
          ),
          elevation: 4.0,
          child: TweenAnimationBuilder(
            tween: Tween<double>(begin: 0.0, end: 1.0),
            duration: Duration(milliseconds: 300),
            builder: (context, double opacity, child) {
              return Opacity(
                opacity: opacity,
                child: child!,
              );
            },
            child: _buildDialogContent(
              context,
              title,
              description,
              dialogType,
              btnOkText,
              btnCancelText,
              onOkPressed,
              onCancelPressed,
            ),
          ),
        );
      },
    );
  }

  static Widget _buildDialogContent(
    BuildContext context,
    String title,
    String description,
    DialogType dialogType,
    String? btnOkText,
    String? btnCancelText,
    Function? onOkPressed,
    Function? onCancelPressed,
  ) {
    Color dialogColor;
    Icon dialogIcon;
    String buttonText = btnOkText ?? "OK";
    String cancelButtonText = btnCancelText ?? "Cancel";

    // Customize appearance based on the DialogType
    switch (dialogType) {
      case DialogType.Success:
        dialogColor = Colors.green;
        dialogIcon = Icon(Icons.check_circle, color: Colors.green, size: 40);
        break;
      case DialogType.Failure:
        dialogColor = Colors.red;
        dialogIcon = Icon(Icons.close_rounded, color: Colors.red, size: 40);
        break;
    }

    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
          dialogIcon,
          SizedBox(height: 16),
          Text(
            title,
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              color: Colors.black,
            ),
          ),
          SizedBox(height: 8),
          Text(
            description,
            style: TextStyle(fontSize: 16, color: Colors.black87),
            textAlign: TextAlign.start,
          ),
          SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              TextButton(
                onPressed: () {
                  if (onCancelPressed != null) {
                    onCancelPressed();
                  }
                  Navigator.of(context).pop(); // Close the dialog
                },
                child: Text(
                  cancelButtonText,
                  style: TextStyle(color: Colors.black),
                ),
              ),
              ElevatedButton(
                onPressed: () {
                  if (onOkPressed != null) {
                    onOkPressed();
                  }
                  Navigator.of(context).pop();
                },
                child: Text(
                  buttonText,
                  style: TextStyle(color: Colors.white),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: dialogColor,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
