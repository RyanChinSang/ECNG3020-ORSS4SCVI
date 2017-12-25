import pyttsx3
'''
Documentation: http://pyttsx3.readthedocs.io/en/latest/engine.html
Reference: 
'''


def on_start(name):
    """
    Fired when the engine begins speaking an utterance.
    :param name: (string) Name associated with the utterance.
    :return:
    """
    if name:
        print('Starting:', name)


def on_word(name, location, length):
    """
    Fired when the engine begins speaking a word.
    :param name: (string) Name associated with the utterance.
    :param location: (integer) The position of the first character of the word in the whole string.
    :param length: (integer) The total number of characters in the word.
    :return:
    """
    if name:
        print('Saying:', gstrg[location:(location + length)])


def on_end(name, completed):
    """
    Fired when the engine finishes speaking an utterance.
    :param name: (string) Name associated with the utterance.
    :param completed: (bool)  True if the utterance was output in its entirety or not.
    :return:
    """
    if name:
        print('Finishing:', name, completed)
    t2s_engine.endLoop()


def on_error(name, exception):
    """
    Fired when the engine encounters an error.
    :param name: (string) Name associated with the utterance.
    :param exception: (Exception) Exception that was raised.
    :return:
    """
    print('aa')
    if exception is RuntimeError:
        pass
    else:
        pass


t2s_engine = pyttsx3.init()
t2s_engine.setProperty('voice', t2s_engine.getProperty('voices')[1].__dict__.get('id'))
t2s_engine.connect('started-utterance', on_start)
t2s_engine.connect('started-word', on_word)
t2s_engine.connect('finished-utterance', on_end)
t2s_engine.connect('error', on_error)
gstrg = ''


def t2s_say(strg, name=None):
    global gstrg
    if name:
        gstrg = strg
    t2s_engine.say(text=strg, name=name)
    try:
        t2s_engine.startLoop()
    except RuntimeError:
        pass


if __name__ == '__main__':
    t2s_say('Hello there, you!', 'hi')
