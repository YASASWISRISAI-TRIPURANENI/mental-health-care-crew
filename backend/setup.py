# backend/setup.py

import nltk
import spacy

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('popular')  # Downloads popular NLTK datasets

# Download Spacy model
spacy.cli.download("en_core_web_sm")
