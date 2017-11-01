# Using an external event loop
import pyttsx3


def externalLoop():
    engine.startLoop(True)
    engine.iterate()
    print("extloop")


engine = pyttsx3.init()
engine.say('The quick brown fox jumped over the lazy dog.', 'fox')
# engine.startLoop(False)
# engine.startLoop(True)
# engine.iterate() must be called inside externalLoop()
externalLoop()
engine.endLoop()


# Not sure how this works
