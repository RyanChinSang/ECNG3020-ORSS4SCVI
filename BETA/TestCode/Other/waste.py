import collections
import itertools
import queue
import threading
from BETA.dev03.models.Txt2Spch import t2s_say
import time

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

# thdr = list(controls_dict.keys())[0]
# maxkey = len(max(list(itertools.chain.from_iterable(
#     [list(list(controls_dict.items())[i][1].keys()) for i in range(len(controls_dict.items()))])), key=len))
# maxline = len(max(
#     [cmd.ljust(maxkey, ' ') + ": " + str(controls_dict.get(hdr).get(cmd)).strip('[]').replace('\'', '') for hdr in
#      controls_dict for cmd in controls_dict.get(hdr)], key=len))
# print([cmd.ljust(maxkey, ' ') + ": " + str(controls_dict.get(hdr).get(cmd)).strip('[]').replace('\'', '') for hdr in
#      controls_dict for cmd in controls_dict.get(hdr)])
# #
# for hdr in controls_dict:
#     for cmd in controls_dict.get(hdr):
#         if hdr != thdr:
#             thdr = hdr
#             rem = maxline - len(hdr)
#             for x in range(rem + 1):
#                 if x == (int(-(-(rem / 2) // 1)) - 1):
#                     print(hdr, end='')
#                 else:
#                     print('_', end='') if x != rem else print('_')
#         print(cmd.ljust(maxkey, ' ') + ': ' + str(controls_dict.get(hdr).get(cmd)).strip('[]').replace('\'', ''))

# print([d.get('all axes') if 'all axes' in d.keys() for d in list(controls_dict.values())])
# print()
# print([cmd.ljust(maxkey, ' ') + ": " + str(controls_dict.get(hdr).get(cmd)).strip('[]').replace('\'', '') for hdr in controls_dict for cmd in controls_dict.get(hdr)])


# print(list(controls_dict.keys())[1:])  # headers
# print(list(controls_dict.get('[DEFAULT CONTROLS]').keys()))  # commands
# print(controls_dict.get('[DEFAULT CONTROLS]').get('quit'))  # controls
# for hdr in controls_dict.keys():
#     if 'DEFAULT' in hdr:
#         print(hdr)

q = queue.Queue()
fstrg = ''

def get_ctrls_t2s(q, header=None):
    global fstrg
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
                # threading.Thread(target=t2s_say, args=(strg, q), daemon=True).start()
                # time.sleep(2)
    # print(fstrg)
    # threading.Thread(target=t2s_say, args=(fstrg, q), daemon=True).start()
    # time.sleep(15)
    # t.start()
    threading.Thread(target=t2s_say, args=(fstrg, q)).start()
    # t.join()
    # while 1:
    #     if t.isAlive:
    #         print(t.isAlive)
    #         pass
    #     else:
    #         break
    #     t = threading.Thread(target=t2s_say, args=(fstrg, q), daemon=True).start()
    #     print(t.get_name()
    #     if threading.Thread.):
    #         pass
    #     else:
    #         break

get_ctrls_t2s(q, header='CUSTOM')

# TODO: make thread exit after t2s action is complete