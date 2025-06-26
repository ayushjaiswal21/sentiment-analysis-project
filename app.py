# app.py
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import pickle
import re
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os

app = Flask(__name__)

# Global variables to store model and tokenizer
model = None
tokenizer = None

def load_model_and_tokenizer():
    """Load the trained model and tokenizer"""
    global model, tokenizer
    
    try:
        # Load model
        model = tf.keras.models.load_model('models/sentiment_model.h5')
        
        # Load tokenizer
        with open('models/tokenizer.pkl', 'rb') as f:
            tokenizer = pickle.load(f)
        
        print("Model and tokenizer loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def clean_text(text):
    """Clean input text"""
    text = re.sub(r'@[\w]+', '', text)       # remove @mentions
    text = re.sub(r'http\S+', '', text)      # remove URLs
    text = re.sub(r'#', '', text)            # remove hashtag symbol
    text = re.sub(r'[^A-Za-z\s]', '', text)  # remove special characters
    text = text.lower().strip()              # convert to lowercase and trim
    return text

def predict_sentiment(text):
    """Predict sentiment for given text"""
    if not model or not tokenizer:
        return None, 0.0
    
    # Clean text
    cleaned_text = clean_text(text)
    
    if not cleaned_text:
        return "Neutral", 0.5
    
    # Convert to sequence
    sequence = tokenizer.texts_to_sequences([cleaned_text])
    padded_sequence = pad_sequences(sequence, maxlen=40, padding='post')
    
    # Predict
    prediction = model.predict(padded_sequence)[0][0]
    
    # Determine sentiment
    if prediction > 0.6:
        sentiment = "Positive 😊"
    elif prediction < 0.4:
        sentiment = "Negative 😞"
    else:
        sentiment = "Neutral 😐"
    
    confidence = float(prediction)
    return sentiment, confidence

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict sentiment for input text"""
    try:
        # Get text from form
        text = request.form.get('text', '').strip()
        
        if not text:
            return render_template('result.html', 
                                 original_text="", 
                                 sentiment="Please enter some text", 
                                 confidence=0.0,
                                 error=True)
        
        # Predict sentiment
        sentiment, confidence = predict_sentiment(text)
        
        if sentiment is None:
            return render_template('result.html', 
                                 original_text=text, 
                                 sentiment="Model not loaded", 
                                 confidence=0.0,
                                 error=True)
        
        return render_template('result.html', 
                             original_text=text, 
                             sentiment=sentiment, 
                             confidence=round(confidence * 100, 2),
                             error=False)
    
    except Exception as e:
        return render_template('result.html', 
                             original_text=text if 'text' in locals() else "", 
                             sentiment=f"Error: {str(e)}", 
                             confidence=0.0,
                             error=True)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for sentiment prediction"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        sentiment, confidence = predict_sentiment(text)
        
        if sentiment is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        return jsonify({
            'text': text,
            'sentiment': sentiment,
            'confidence': round(confidence * 100, 2)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load model and tokenizer on startup
    if not os.path.exists('models/sentiment_model.h5'):
        print("Model not found! Please run model_trainer.py first.")
        print("Make sure you have the dataset in data/ folder.")
    else:
        load_model_and_tokenizer()
    
    app.run(debug=True, host='0.0.0.0', port=5000)