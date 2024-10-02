// lib/widgets/chat_bubble.dart

import 'package:flutter/material.dart';
import '../models/message.dart';
import 'package:intl/intl.dart';

class ChatBubble extends StatelessWidget {
  final Message message;

  ChatBubble({required this.message});

  @override
  Widget build(BuildContext context) {
    bool isUser = message.sender == 'user';
    Alignment alignment = isUser ? Alignment.centerRight : Alignment.centerLeft;
    Color bubbleColor = isUser ? Colors.blue[100]! : Colors.grey[300]!;
    CrossAxisAlignment crossAxisAlignment = isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start;

    return Container(
      margin: EdgeInsets.symmetric(vertical: 5, horizontal: 10),
      alignment: alignment,
      child: Column(
        crossAxisAlignment: crossAxisAlignment,
        children: [
          Container(
            padding: EdgeInsets.all(10),
            constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.7),
            decoration: BoxDecoration(
              color: bubbleColor,
              borderRadius: BorderRadius.circular(10),
            ),
            child: Text(
              message.text,
              style: TextStyle(fontSize: 16),
            ),
          ),
          SizedBox(height: 5),
          Text(
            DateFormat('h:mm a').format(message.time),
            style: TextStyle(fontSize: 10, color: Colors.grey),
          ),
        ],
      ),
    );
  }
}
