// lib/models/message.dart

class Message {
  final String sender; // 'user' or 'bot'
  final String text;
  final DateTime time;

  Message({
    required this.sender,
    required this.text,
    required this.time,
  });
}
