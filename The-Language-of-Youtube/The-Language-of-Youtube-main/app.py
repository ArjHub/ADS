from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
from scipy.sparse import csr_matrix
import re
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the saved model
filename = './Model/svm_model.pkl'
loaded_model = pickle.load(open(filename, 'rb'))


def preprocess_text(text):
    # Remove HTML tags
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-z\s]', '', text)

    # Tokenization
    tokens = word_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]

    # Join tokens back into a string
    processed_text = ' '.join(tokens)

    return processed_text


# Create your Flask app
app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template('yoshi.html')


@app.route('/predict', methods=["POST"])
def predict_genre():
    title = request.form.get('video-title')
    description = request.form.get('video-description')
    title = preprocess_text(title)
    description = preprocess_text(description)
    print(title)
    print(description)
    tfidf = pickle.load(open('./Model/tfidf.pkl', 'rb'))
    feed = tfidf.transform([title + ' ' + description])
    genre = loaded_model.predict(feed)[0]
    return render_template('output.html', y=genre)


if __name__ == '__main__':
    app.run(debug=True)
