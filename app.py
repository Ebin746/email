from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re

# Load trained model and vectorizer
model = joblib.load("spam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

app = Flask(__name__)
CORS(app)

# Cleaning function same as used in training
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Check for 'message' in input
    if not data or 'message' not in data:
        return jsonify({'error': 'Missing "message" in request'}), 400

    message = data['message']
    cleaned = clean_text(message)
    vect = vectorizer.transform([cleaned])
    prediction = model.predict(vect)[0]

    return jsonify({'result': 'Spam' if prediction == 1 else 'Not Spam'})

if __name__ == '__main__':
    app.run(debug=True)

