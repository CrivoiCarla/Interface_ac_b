import pyaudio
import azure.cognitiveservices.speech as speechsdk

class AudioManager:
    def __init__(self, sample_rate, channels, format):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=format,
                                      channels=channels,
                                      rate=sample_rate,
                                      output=True)

    def play_audio(self, audio_data):     
        self.stream.write(audio_data)

# increase sample rate to increase voice speed
audio_manager = AudioManager(sample_rate=18000, channels=1, format=pyaudio.paInt16)

class PushAudioOutputStreamSampleCallback(speechsdk.audio.PushAudioOutputStreamCallback):
    """
    Example class that implements the PushAudioOutputStreamCallback, which is used to show
    how to push output audio to a stream
    """
    def __init__(self) -> None:
        super().__init__()
        self._closed = False

    def write(self, audio_buffer: memoryview) -> int:
        """
        The callback function which is invoked when the synthesizer has an output audio chunk
        to write out
        """
        audio_manager.play_audio(audio_buffer.tobytes())
        return audio_buffer.nbytes

    def close(self) -> None:
        """
        The callback function which is invoked when the synthesizer is about to close the
        stream.
        """
        self._closed = True
        print("Push audio output stream closed.")

class TextToSpeech:
    def __init__(self, speech_config):  
        stream_callback = PushAudioOutputStreamSampleCallback()
        self.push_stream = speechsdk.audio.PushAudioOutputStream(stream_callback)
        stream_config = speechsdk.audio.AudioOutputConfig(stream=self.push_stream)
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=stream_config)
  

    def speak_text_async(self, evt: speechsdk.SpeechRecognitionEventArgs):
        print('RECOGNIZED: {}'.format(evt.result.text))
        self.speech_synthesizer.speak_text_async(evt.result.text)
        # self.speech_synthesizer.speak_text(evt.result.text)
        # self.speech_synthesizer.start_speaking_text(evt.result.text)
