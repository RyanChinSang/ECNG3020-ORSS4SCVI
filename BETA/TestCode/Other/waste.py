import collections
import itertools
import queue
import threading
from BETA.dev03.models.Txt2Spch import t2s_say
import time
import multiprocessing
import _thread

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
        'check online': ['z'],
        'color check': ['m'],
        'force offline': ['x'],
        'object check': ['n', 'a', 'c'],  # NOTE 'a' here is just a test case - REMOVE WHEN DONE
        'object check 2': ['ctrl+n']
    })
])

q = queue.Queue()


def get_ctrls(q, header=None):
    fstrg = ''
    for hdr in controls_dict.keys():
        if header in hdr:
            commands = list(controls_dict.get(hdr).keys())
            for cmd in commands:
                ctrls = controls_dict.get(hdr).get(cmd)
                strg = 'To \'' + cmd + '\', press \''
                for x in range(len(ctrls)):
                    strg += ctrls[x]
                    if x < len(ctrls) - 1:
                        strg += '\', or \''
                    else:
                        strg += '\'. '
                fstrg += strg
    q.put(fstrg)


get_ctrls(q, header='CUSTOM')

