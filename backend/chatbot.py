# backend/chatbot.py

from flask import Blueprint, request, jsonify
from flask_cors import CORS
import requests
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import json
import random
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector

chatbot_bp = Blueprint('chatbot', __name__)

# Load the trained model and data
model = load_model('model.h5')
with open('texts.pkl', 'rb') as f:
    words = pickle.load(f)
with open('labels.pkl', 'rb') as f:
    classes = pickle.load(f)
with open('intents.json') as f:
    intents = json.load(f)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Setup Spacy for language detection
def get_lang_detector(nlp, name):
    return LanguageDetector()
nlp = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)

# Initialize translation pipelines
eng_swa_model_checkpoint = "Helsinki-NLP/opus-mt-en-swc"
eng_swa_tokenizer = AutoTokenizer.from_pretrained("./model/eng_swa_model/")
eng_swa_model = AutoModelForSeq2SeqLM.from_pretrained("./model/eng_swa_model/")
eng_swa_translator = pipeline(
    "text2text-generation",
    model=eng_swa_model,
    tokenizer=eng_swa_tokenizer,
)

def translate_text_eng_swa(text):
    translated_text = eng_swa_translator(text, max_length=128, num_beams=5)[0]['generated_text']
    return translated_text

swa_eng_model_checkpoint = "Helsinki-NLP/opus-mt-swc-en"
swa_eng_tokenizer = AutoTokenizer.from_pretrained("./model/swa_eng_model/")
swa_eng_model = AutoModelForSeq2SeqLM.from_pretrained("./model/swa_eng_model/")
swa_eng_translator = pipeline(
    "text2text-generation",
    model=swa_eng_model,
    tokenizer=swa_eng_tokenizer,
)

def translate_text_swa_eng(text):
    translated_text = swa_eng_translator(text, max_length=128, num_beams=5)[0]['generated_text']
    return translated_text

# Define bag of words
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)

    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print(f"found in bag: {w}")

    return np.array(bag)

def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    if ints:
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result
    else:
        return "Sorry, I didn't understand that."

def chatbot_response(msg):
    doc = nlp(msg)
    detected_language = doc._.language['language']
    print(f"Detected language chatbot_response:- {detected_language}")

    chatbotResponse = "Loading bot response..........."

    if detected_language == "en":
        res = getResponse(predict_class(msg, model), intents)
        chatbotResponse = res
        print("en_sw chatbot_response:- ", res)
    elif detected_language == 'sw':
        translated_msg = translate_text_swa_eng(msg)
        res = getResponse(predict_class(translated_msg, model), intents)
        chatbotResponse = translate_text_eng_swa(res)
        print("sw_en chatbot_response:- ", chatbotResponse)
    else:
        # Handle other languages or default to English
        res = getResponse(predict_class(msg, model), intents)
        chatbotResponse = res

    return chatbotResponse

# Gemini API Configuration
GEMINI_API_URL = 'https://gemini.api.url/651ce1cc-830c-4793-8926-fac6905bd341'  # Replace with actual Gemini API URL
GEMINI_API_KEY = 'AIzaSyCmCpoOveD0btqCWsU5wzUfpjz6oLUrWdc'  # Replace with your Gemini API key

def call_gemini_api(text):
    """
    Function to call Gemini API for enhanced NLP tasks.
    Replace the URL and headers with your Gemini API details.
    """
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text
        # Add other required parameters as per Gemini API documentation
    }
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()  # Adjust based on Gemini API's response structure
        else:
            print(f"Gemini API Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None

@chatbot_bp.route('/response', methods=['POST'])
def get_bot_response():
    user_message = request.json.get('message')
    print(f"Received message: {user_message}")

    # Optional: Use Gemini API to enhance or preprocess the message
    gemini_response = call_gemini_api(user_message)
    if gemini_response and 'enhanced_text' in gemini_response:
        enhanced_message = gemini_response['enhanced_text']
    else:
        enhanced_message = user_message

    bot_response = chatbot_response(enhanced_message)

    # Optional: Further process the bot_response with Gemini API for emotion detection
    # Example:
    # emotion_response = call_gemini_api(bot_response)
    # if emotion_response and 'emotion' in emotion_response:
    #     detected_emotion = emotion_response['emotion']
    #     # Modify bot_response based on detected_emotion
    #     if detected_emotion == 'sadness':
    #         bot_response += " I'm really sorry you're feeling this way. Please reach out to a mental health professional or someone you trust."
    #     elif detected_emotion == 'stress':
    #         bot_response += " It sounds like you're stressed. Remember to take deep breaths and take breaks."
    #     # Add more conditions as needed

    return jsonify({'response': bot_response})
