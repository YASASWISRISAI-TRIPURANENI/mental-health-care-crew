// lib/screens/chat_screen.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/chat_provider.dart';
import '../widgets/chat_bubble.dart';
import '../widgets/message_input.dart';
import 'package:flutter_svg/flutter_svg.dart';

class ChatScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // App Bar with Title and Icon
      appBar: AppBar(
        title: Row(
          children: [
            SvgPicture.asset(
              'assets/svg/robot.svg', // Path to your robot SVG
              width: 30,
              height: 30,
              color: Colors.white,
            ),
            SizedBox(width: 10),
            Text('Psychiatrist Bot'),
          ],
        ),
        backgroundColor: Colors.blue,
      ),
      // Chat Messages and Input
      body: Column(
        children: [
          // Chat Messages
          Expanded(
            child: Consumer<ChatProvider>(
              builder: (context, chatProvider, child) {
                return ListView.builder(
                  reverse: true,
                  padding: EdgeInsets.all(10),
                  itemCount: chatProvider.messages.length,
                  itemBuilder: (context, index) {
                    // Display messages in reverse order
                    var message = chatProvider.messages[chatProvider.messages.length - 1 - index];
                    return ChatBubble(message: message);
                  },
                );
              },
            ),
          ),
          // Input Field
          MessageInput(),
        ],
      ),
    );
  }
}
