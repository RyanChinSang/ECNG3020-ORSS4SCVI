import pyttsx3
import multiprocessing


def on_start(name):
    """
    Fired when the engine begins speaking an utterance.
    :param name: (string) Name associated with the utterance.
    :return:
    """
    pass


def on_word(name, location, length):
    """
    Fired when the engine begins speaking a word.
    :param name: (string) Name associated with the utterance.
    :param location: (integer) T
    :param length: (integer) 
    :return:
    """
    pass


def on_end(name, completed):
    """
    Fired when the engine finishes speaking an utterance.
    :param name: (string) Name associated with the utterance.
    :param completed: (bool)  True if the utterance was output in its entirety or not.
    :return:
    """
    t2s_engine.endLoop()
    return


def on_error(name, exception):
    """
    Fired when the engine encounters an error.
    :param name: (string) Name associated with the utterance.
    :param exception: (Exception) Exception that was raised.
    :return:
    """
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


def t2s_start(word):
    t2s_engine.say(word)
    t2s_engine.startLoop()


def t2s_say(word):
    multiprocessing.Process(target=t2s_start, args=(word,)).start()


if __name__ == '__main__':
    t2s_say('hi')
