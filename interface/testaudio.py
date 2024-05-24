import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("Streaming...")

try:
    while True:
        data = stream.read(CHUNK)
        print(data)
        stream.write(data, CHUNK)
except KeyboardInterrupt:
    print("Streaming stopped")

stream.stop_stream()
stream.close()
p.terminate()
