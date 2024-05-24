import keyboard
import subprocess
import sys
from STT import SpeechToText
from TTS import TextToSpeech
import azure.cognitiveservices.speech as speechsdk


if __name__ == '__main__':


    speech_key, service_region = "16200612f681448ca6cd8870d82ea638", "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    text_to_speech = TextToSpeech(speech_config)

    speech_to_text = SpeechToText(speech_config, text_to_speech.speak_text_async)

    speech_to_text.start_continuous_recognition_async()

