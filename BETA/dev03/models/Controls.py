import collections
import itertools

controls_dict = collections.OrderedDict([
    # active keys: a,c,v,f,g,G,g,h,r,p,q,W,Q,s,k,L,l,o,b,d
    # e,t,y,u,i
    # d,j
    # [z],[x],[b],[n],[m]
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
        'object check': ['n'],  # NOTE 'a' here is just a test case - REMOVE WHEN DONE
        'object check 2': ['ctrl+n'],
        'say controls': ['b'],
        'say controls 2': ['ctrl+b']
    })
])


def print_ctrls(header=None):
    thdr = list(controls_dict.keys())[0]
    maxkey = len(max(list(itertools.chain.from_iterable(
        [list(list(controls_dict.items())[i][1].keys()) for i in range(len(controls_dict.items()))])), key=len))
    maxline = len(max(
        [cmd.ljust(maxkey, ' ') + ": " + str(controls_dict.get(hdr).get(cmd)).strip('[]').replace('\'', '') for hdr in
         controls_dict for cmd in controls_dict.get(hdr)], key=len))
    for hdr in controls_dict:
        if hdr == header:
            rem = maxline - len(hdr)
            for x in range(rem + 1):
                if x == (int(-(-(rem / 2) // 1)) - 1):
                    print(hdr, end='')
                else:
                    print('_', end='') if x != rem else print('_')
            for cmd in controls_dict.get(hdr):
                print(cmd.ljust(maxkey, ' ') + ': ' + str(controls_dict.get(hdr).get(cmd)).strip('[]').replace('\'', ''))
        elif header is None:
            for cmd in controls_dict.get(hdr):
                if hdr != thdr:
                    thdr = hdr
                    rem = maxline - len(hdr)
                    for x in range(rem + 1):
                        if x == (int(-(-(rem / 2) // 1)) - 1):
                            print(hdr, end='')
                        else:
                            print('_', end='') if x != rem else print('_')
                print(cmd.ljust(maxkey, ' ') + ': ' + str(controls_dict.get(hdr).get(cmd)).strip('[]').replace('\'', ''))


def fetch_ctrls(command, q):
    for hdr in controls_dict:
        if controls_dict.get(hdr).get(command):
            return q.put(controls_dict.get(hdr).get(command))


def get_ctrls_t2s(q, header=None):
    pass


if __name__ == '__main__':
    import queue
    import threading
    q = queue.Queue()
    print(q.get(threading.Thread(target=fetch_ctrls, args=('quit', q), daemon=True).start()))
    # if 'q' in q.get(threading.Thread(target=fetch_ctrls, args=('quit', q), daemon=True).start()):
    #     print('ye')
    print_ctrls('[DEFAULT CONTROLS]')
