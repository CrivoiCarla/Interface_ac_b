import azure.cognitiveservices.speech as speechsdk

class SpeechToText:
    def __init__(self, speech_config, callback_func):
        speech_config.set_property(speechsdk.PropertyId.Speech_SegmentationSilenceTimeoutMs, "100") 
        self.callback_tts = callback_func
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
        self.done = False

    # def recognized_cb(self, evt: speechsdk.SpeechRecognitionEventArgs):
    #     print('RECOGNIZED: {}'.format(evt.result.text))
    #     self.callback_tts(evt.result.text)

    def stop_cb(self, evt: speechsdk.SessionEventArgs):
        print('CLOSING on {}'.format(evt))
        self.done = True

    def start_continuous_recognition_async(self):
        self.speech_recognizer.recognized.connect(self.callback_tts)
        self.speech_recognizer.session_stopped.connect(self.stop_cb)
        self.speech_recognizer.canceled.connect(self.stop_cb)
        result_future = self.speech_recognizer.start_continuous_recognition_async()
        result_future.get()
        print('Continuous Recognition is now running, say something.')

        # while not self.done:
        #     print('type "stop" then enter when done')
        #     stop = input()
        #     if stop.lower() == "stop":
        #         print('Stopping async recognition.')
        #         self.speech_recognizer.stop_continuous_recognition_async()
        #         break
        #
        # print("Recognition stopped")