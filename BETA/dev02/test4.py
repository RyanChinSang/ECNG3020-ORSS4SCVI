import pyttsx3

t2s_engine = pyttsx3.init()
t2s_engine.setProperty('voice', t2s_engine.getProperty('voices')[1].__dict__.get('id'))


def t2s_say(word, q):
    t2s_engine.say(q.get())
    try:
        t2s_engine.runAndWait()
    except RuntimeError:
        pass
