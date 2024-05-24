from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import threading
import time
import keyboard
import subprocess
import sys
import azure.cognitiveservices.speech as speechsdk
from TTS import TextToSpeech
from STT import SpeechToText

app = Flask(__name__)
socketio = SocketIO(app)

class SpeechRecognitionThread(threading.Thread):
    def __init__(self, speech_config):
        super().__init__()
        self.speech_config = speech_config
        self.text_to_speech = TextToSpeech(speech_config)
        self.speech_to_text = SpeechToText(speech_config, self.text_to_speech.speak_text_async)
        self.running = False

    def run(self):
        self.speech_to_text.start_continuous_recognition_async()

@app.route('/')
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
    global speech_recognition_thread
    if not speech_recognition_thread or not speech_recognition_thread.running:
        speech_recognition_thread = SpeechRecognitionThread(speech_config)
        speech_recognition_thread.start()
        return "Speech recognition started."
    else:
        return "Speech recognition already running."

@app.route('/stop', methods=['POST'])
def stop():
    global speech_recognition_thread
    if speech_recognition_thread and speech_recognition_thread.is_alive():
        SpeechToText.speech_recognizer.stop_continuous_recognition_async()
        speech_recognition_thread = None
        return "Speech recognition stopped."
    else:
        return "Speech recognition is not running."

def emit_recognized_text(text):
    socketio.emit('recognized_text', {'text': text})

if __name__ == '__main__':
    speech_key, service_region = "16200612f681448ca6cd8870d82ea638", "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognition_thread = None
    socketio.run(app, debug=True , allow_unsafe_werkzeug=True)
