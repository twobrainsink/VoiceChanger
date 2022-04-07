import pyaudio
import numpy as np

RATE    = 16000
CHUNK   = 256

p = pyaudio.PyAudio()

player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, 
frames_per_buffer=CHUNK)
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

while True: #do this for 10 seconds
    player.write(np.fromstring(stream.read(CHUNK),dtype=np.int16),CHUNK)

stream.stop_stream()
stream.close()
p.terminate()