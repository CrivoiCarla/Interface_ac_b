from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import threading
import time
import keyboard
import subprocess
import sys
import azure.cognitiveservices.speech as speechsdk
from TTS import TextToSpeech
from STT import SpeechToText


speech_config = ""
app = Flask(__name__)
socketio = SocketIO(app)



@app.route('/index')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/start', methods=['POST'])
def start():
    global speech_recognition_thread , speech_config
    with open('recognized_text.txt', 'w') as file:
        file.write("")
    with open('selected_voice.txt', 'r') as file:
        text = file.read()
        if "Male" in text:
            voice = "en-US-BrianMultilingualNeural"
        else:
            voice = "en-US-AvaMultilingualNeural"

        print(text, voice)
    speech_config.set_property(
        property_id=speechsdk.PropertyId.SpeechServiceConnection_SynthVoice,
        value=voice)

    speech_recognition_thread = True
    with open('stop.txt', 'w') as file:
        file.write("")
    text_to_speech = TextToSpeech(speech_config)
    speech_to_text = SpeechToText(speech_config, text_to_speech.speak_text_async)
    speech_to_text.start_continuous_recognition_async( not speech_recognition_thread)

    return "It's run"


@app.route('/stop', methods=['POST'])
def stop():
    with open('stop.txt', 'w') as file:
        file.write("stop")
    return "STOP"


@app.route('/select_voice', methods=['POST'])
def select_voice():
    voice = request.form['voice']
    with open('selected_voice.txt', 'w') as file:
        file.write(voice)
    return 'Voice selected', 200


@app.route('/get_text', methods=['GET'])
def get_text():
    with open('recognized_text.txt', 'r') as file:
        text = file.read()
    return jsonify({"text": text})

@app.route('/')
def voice():
    return render_template('voice.html')

def emit_recognized_text(text):
    socketio.emit('recognized_text', {'text': text})


if __name__ == '__main__':
    speech_key, service_region = "16200612f681448ca6cd8870d82ea638", "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognition_thread = False
    socketio.run(app, debug=True , allow_unsafe_werkzeug=True)


