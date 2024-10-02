// lib/providers/chat_provider.dart

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/message.dart';

class ChatProvider with ChangeNotifier {
  List<Message> _messages = [];

  List<Message> get messages => _messages;

  // Replace with your actual Flask backend URL
  final String backendUrl = 'http://YOUR_FLASK_BACKEND_URL/api/chatbot/response';

  Future<void> sendMessage(String message) async {
    // Add user message to the conversation
    _messages.add(Message(sender: 'user', text: message, time: DateTime.now()));
    notifyListeners();

    try {
      final response = await http.post(
        Uri.parse(backendUrl),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'message': message}),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        String botMessage = data['response'];
        _messages.add(Message(sender: 'bot', text: botMessage, time: DateTime.now()));
      } else {
        _messages.add(Message(sender: 'bot', text: "Sorry, I couldn't process that.", time: DateTime.now()));
      }
    } catch (error) {
      _messages.add(Message(sender: 'bot', text: "An error occurred. Please try again.", time: DateTime.now()));
    }

    notifyListeners();
  }
}
