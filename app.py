from flask import Flask, request, render_template
import tensorflow as tf
import re
import string
from tensorflow import keras
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def custom_standardization(input_data):
    """Clean and transform input data to lowercase

    # Arguments
        input_data: tweet to clean.
    """
    lowercase = tf.strings.lower(input_data)
    remove_colors = tf.strings.regex_replace(lowercase, '&#\d+;', '')
    remove_hex = tf.strings.regex_replace(remove_colors, r'[^\x00-\x7f]', r'')
    remove_url = tf.strings.regex_replace(remove_hex, 'http.+$', '')
    remove_puntuation = tf.strings.regex_replace(remove_url, '[%s]' % re.escape(string.punctuation), '')
    remove_amp = tf.strings.regex_replace(remove_puntuation, '&amp;', '')
    return tf.strings.regex_replace(remove_amp, 'http.+$', '')


model = keras.models.load_model('hate_speech_model',
                                custom_objects={'TextVectorization': TextVectorization,
                                                'custom_standardization': custom_standardization})

@app.route('/')
def root():
    print("Render index")
    return render_template('index.html')

@app.route("/validate", methods=["POST"])
def validate():
    print("Request received")
    tweet = request.json
    print("Tweet: " + tweet['tweet'])
    prediction = model.predict([str(tweet['tweet'])])
    is_hate_speech = not(prediction[0][0] > 0.5)
    print("Response:  " + str(is_hate_speech))
    return str(is_hate_speech).lower()
