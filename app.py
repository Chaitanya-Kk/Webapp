from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import spacy
import json

# Initialize the Flask app
app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load knowledge base
def load_knowledge_base(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"questions": []}

# Normalize input
def normalize_input(user_input):
    normalized = user_input.strip().capitalize()
    tokens = [token.text for token in nlp(normalized)]
    return normalized, tokens

# Sentiment analysis
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

# Check for greetings
def is_greeting(user_input):
    greetings = ['hello', 'hi', 'hey']
    return any(greeting in user_input.lower() for greeting in greetings)

# Find best match for questions
def find_best_match(user_question, questions):
    user_tokens = set([token.text.lower() for token in nlp(user_question)])
    question_matches = {}

    for question in questions:
        question_tokens = set([token.text.lower() for token in nlp(question)])
        overlap = user_tokens.intersection(question_tokens)
        if overlap:
            question_matches[question] = len(overlap) / len(question_tokens)

    return max(question_matches, key=question_matches.get, default=None)

# Get bot response
def get_bot_response(user_input, knowledge_base):
    normalized_input, _ = normalize_input(user_input)
    best_match = find_best_match(normalized_input, [q['question'] for q in knowledge_base['questions']])

    if best_match:
        return next(q['answer'] for q in knowledge_base['questions'] if q['question'] == best_match)
    else:
        return "I don't know the answer. Can you teach me?"

# Home route
@app.route('/')
def home():
    return render_template('chat.html')

# API for chat interaction
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')

    if not user_input:
        return jsonify({"response": "Please enter a message."})

    knowledge_base = load_knowledge_base('knowledge_base.json')

    if is_greeting(user_input):
        response = "Hello! 😊 How can I assist you today?"
    else:
        sentiment_polarity, _ = get_sentiment(user_input)
        response = get_bot_response(user_input, knowledge_base)

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
