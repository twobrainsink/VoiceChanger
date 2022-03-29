from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import wave
from threading import Thread


filename = "recorded.wav"

output = []

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                output=True,
                frames_per_buffer=1024)


def change_voice():
    i = 0
    while True:
        if len(output) > i:
            wf = wave.open(filename, "wb")

            wf.setnchannels(1)

            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))

            wf.setframerate(44100)

            wf.writeframes(b"".join(output[i]))

            wf.close()

            sound_before = AudioSegment.from_file(filename, "wav")

            octaves = -0.5

            new_sample_rate = int(sound_before.frame_rate * (2.0 ** octaves))

            ton_effect = sound_before._spawn(sound_before.raw_data, overrides={'frame_rate': new_sample_rate})
            play(ton_effect)
            del output[0]
        else:
            i = 0

def record():
    while True:
        frames = []
        print("Recording...")
        for i in range(50):
            data = stream.read(1024)
            frames.append(data)
        print("Finished recording.")
        output.append(frames)

recod_t = Thread(target=record)
play_t = Thread(target=change_voice)

recod_t.start()
play_t.start()
recod_t.join()
play_t.join()



