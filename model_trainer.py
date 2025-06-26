# model_trainer.py
import pandas as pd
import numpy as np
import re
import pickle
import os
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense, Dropout
from sklearn.model_selection import train_test_split

def clean_text(text):
    """Clean tweet text"""
    text = re.sub(r'@[\w]+', '', text)       # remove @mentions
    text = re.sub(r'http\S+', '', text)      # remove URLs
    text = re.sub(r'#', '', text)            # remove hashtag symbol
    text = re.sub(r'[^A-Za-z\s]', '', text)  # remove special characters
    text = text.lower().strip()              # convert to lowercase and trim
    return text

def load_and_preprocess_data():
    """Load and preprocess the dataset"""
    print("Loading dataset...")
    
    # Load the dataset
    df = pd.read_csv("data/training.1600000.processed.noemoticon.csv", 
                     encoding='latin-1', header=None)
    
    # Rename columns
    df.columns = ['sentiment', 'id', 'date', 'query', 'user', 'text']
    
    # Keep only relevant columns
    df = df[['sentiment', 'text']]
    
    # Convert sentiment: 0 = negative, 4 = positive → make 4 → 1
    df['sentiment'] = df['sentiment'].map({0: 0, 4: 1})
    
    # Clean text
    df['clean_text'] = df['text'].apply(clean_text)
    
    print(f"Dataset shape: {df.shape}")
    return df

def create_tokenizer_and_sequences(df):
    """Create tokenizer and convert text to sequences"""
    print("Creating tokenizer and sequences...")
    
    # Tokenizer
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(df['clean_text'])
    
    # Convert text to sequences
    sequences = tokenizer.texts_to_sequences(df['clean_text'])
    
    # Pad sequences
    padded = pad_sequences(sequences, maxlen=40, padding='post', truncating='post')
    
    return tokenizer, padded

def build_model():
    """Build the RNN model"""
    print("Building model...")
    
    model = Sequential()
    model.add(Embedding(input_dim=10000, output_dim=64, input_length=40))
    model.add(SimpleRNN(64, return_sequences=False))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model():
    """Main training function"""
    # Create directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Load data
    df = load_and_preprocess_data()
    
    # Create tokenizer and sequences
    tokenizer, X = create_tokenizer_and_sequences(df)
    y = df['sentiment'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Build model
    model = build_model()
    
    print("Training model...")
    history = model.fit(X_train, y_train, epochs=3, batch_size=128, 
                       validation_data=(X_test, y_test), verbose=1)
    
    # Evaluate model
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Accuracy: {accuracy:.4f}")
    
    # Save model and tokenizer
    model.save('models/sentiment_model.h5')
    
    with open('models/tokenizer.pkl', 'wb') as f:
        pickle.dump(tokenizer, f)
    
    print("Model and tokenizer saved successfully!")
    return model, tokenizer

if __name__ == "__main__":
    train_model()