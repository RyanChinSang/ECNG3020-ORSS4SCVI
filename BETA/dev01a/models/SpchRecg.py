import speech_recognition as sr
import socket
from threading import Thread

GOOGLE_SPEECH_RECOGNITION_API_KEY = None


def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False


def google_sr(audio, key=GOOGLE_SPEECH_RECOGNITION_API_KEY):
    try:
        print(sr.Recognizer().recognize_google(audio, key))
        text = str(sr.Recognizer().recognize_google(audio, key))
        return text
    except sr.UnknownValueError:
        # return "Google Speech Recognition could not understand audio"
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        # return "Could not request results from Google Speech Recognition service; {0}".format(e)
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    # return word


def sphinx_sr(audio):
    try:
        # print("Sphinx thinks you said: " + sr.Recognizer().recognize_sphinx(audio))
        print(sr.Recognizer().recognize_sphinx(audio))
        return str(sr.Recognizer().recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


if __name__ == '__main__':
    while True:
        # obtain audio from the microphone
        with sr.Microphone(device_index=0) as source:
            # print("Say something!")
            audio = sr.Recognizer().listen(source)
        if internet():
            Thread(target=google_sr, args=(audio,), daemon=True).start()
        else:
            Thread(target=sphinx_sr, args=(audio,), daemon=True).start()
