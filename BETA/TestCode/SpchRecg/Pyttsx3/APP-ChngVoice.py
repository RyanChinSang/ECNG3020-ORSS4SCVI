# Changing voices
import pyttsx3

engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# print(len(voices))
# print(voices[0].__dict__)
# print(voices[1].__dict__.get('id'))
# for voice in voices:
#     engine.setProperty('voice', voice.id)
engine.setProperty('voice', engine.getProperty('voices')[1].__dict__.get('id'))
engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()
