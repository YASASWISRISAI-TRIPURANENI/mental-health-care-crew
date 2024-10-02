# backend/app.py

from flask import Flask
from flask_cors import CORS
from chatbot import chatbot_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

if __name__ == '__main__':
    app.run(debug=True)
