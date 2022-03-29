from pydub import AudioSegment
from pydub.playback import play
from threading import Thread
import asyncio
import speech_recognition
import pyaudio
import wave
from _thread import start_new_thread

out = []
filename = "recorded.wav"
p = pyaudio.PyAudio()
r = speech_recognition.Recognizer()
micro = speech_recognition.Microphone()

def change_voice():
    i = 0
    while True:
        try:
            
            f = wave.open(filename, "wb")
            f.setnchannels(1)

            f.setsampwidth(p.get_sample_size(pyaudio.paInt16))

            f.setframerate(44100)
            f.writeframes(out[i].get_wav_data())
            f.close()   
            sound_before = AudioSegment.from_file(filename, "wav")

            octaves = -0.5

            new_sample_rate = int(sound_before.frame_rate * (2.0 ** octaves))

            ton_effect = sound_before._spawn(sound_before.raw_data, overrides={'frame_rate': new_sample_rate})
            play(ton_effect)
            out.remove(out[i])
        except:
            pass


def check(a):
    try:
        text = r.recognize_google(a, language="ru")
        out.append(a)
    except:
        pass

def record():
    while True:
        with micro as source:
            r.adjust_for_ambient_noise(source)
            try:
                print("listen")
                a = r.listen(source, timeout=0.08)
                start_new_thread(check, (a, ))
                continue
            except:
                pass

   
recod_t = Thread(target=record)
play_t = Thread(target=change_voice)

recod_t.start()
play_t.start()
recod_t.join()
play_t.join()
