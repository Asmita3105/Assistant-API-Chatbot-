from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from assistant import Assistant  # Ensure that Chatbot class/method is properly defined in assistant.py

# Load environment variables from .env file
load_dotenv('/mnt/data/.env')

# Initialize Flask app
app = Flask(__name__)

# Initialize the chatbot
chatbot = Assistant()

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    response = chatbot.get_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
