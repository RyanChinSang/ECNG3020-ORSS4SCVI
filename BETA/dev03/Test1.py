import pyttsx3
import collections
import itertools

controls_dict = collections.OrderedDict([
    # active keys: a,c,v,f,g,G,g,h,r,p,q,W,Q,s,k,L,l,o,b,d
    # e,t,y,u,i
    # d,j
    # [z],[x],b,[n],[m]
    ('header', {
        #     'command': ['control']
    }),
    ('[DEFAULT CONTROLS]', {
        'all axes': ['a'],
        'back': ['left', 'c', 'backspaces'],
        'forward': ['right', 'v'],
        'fullscreen': ['f', 'ctrl+f'],
        'grid': ['g'],
        'grid minor': ['G'],
        'home': ['h', 'r', 'home'],
        'pan': ['p'],
        'quit': ['ctrl+w', 'cmd+w', 'q'],
        'quit all': ['W', 'cmd+W', 'Q'],
        'save': ['s', 'ctrl+s'],
        'xscale': ['k', 'L'],
        'yscale': ['l'],
        'zoom': ['o']
    }),
    ('[CUSTOM CONTROLS]', {
        'color check': ['m'],
        'offline force': ['x'],
        'object check': ['n'],
        'object check 2': ['ctrl+n'],
        'online check': ['z']
    })
])


t2s_engine = pyttsx3.init()
t2s_engine.setProperty('voice', t2s_engine.getProperty('voices')[1].__dict__.get('id'))


def t2s_say(word, q):
    t2s_engine.say(word)
    try:
        t2s_engine.runAndWait()
    except RuntimeError:
        pass


if __name__ == '__main__':
    import queue
    q = queue.Queue()
    # s ='[DEFAULT CONTROLS]'
    s = "To 'object check 2', press 'ctrl+n'."
    t2s_say(s, q)