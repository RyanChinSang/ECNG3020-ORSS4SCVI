from gtts import gTTS
import os

# tts = gTTS(text='The quick brown fox jumped over the lazy dog', lang='en', slow=True)
tts = gTTS(text='The quick brown fox jumped over the lazy dog', lang='en')
# for obj in tts:
#     print(obj)
print(tts)
print(tts.__dict__)
print(tts.token.__dict__)
tts.save("hello.mp3")
os.system("hello.mp3 -quiet")