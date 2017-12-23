import collections
import itertools

ctrls_dict = collections.OrderedDict([
    # symbols: "-" = ctrl, "+" = cmd, "[]" = custom key that is in use
    # active keys: a,c,v,-f,g,G,g,h,r,p,-+w,-W,q,Q,-s,k,L,l,o,b,d
    # e,t,y,u,i
    # d,j
    # [z],[x],[-b],[-n],[m]
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
        'object check': ['n'],
        'object check 2': ['ctrl+n'],
        'say controls': ['b'],
        'say controls 2': ['ctrl+b']
    })
])

sctrls_dict = collections.OrderedDict([
    # Spoken [Online] commands
    # (cmd, {decription: [keywords]})
    ('color check', {'check the color': ['what', 'color']}),
    ('force offline', {'activate offline mode': ['go', 'offline']}),
    ('object check', {'say the name of the object': ['what', 'object']}),
    ('quit', {'exit the program': ['quit', 'exit']}),
    ('say controls', {'repeat what the controls are': ['what', 'controls']}),
    ('save', {'take a snapshot': ['take', 'picture']})
])


def print_ctrls(header=None):
    thdr = list(ctrls_dict.keys())[0]
    maxkey = len(max(list(itertools.chain.from_iterable(
        [list(list(ctrls_dict.items())[i][1].keys()) for i in range(len(ctrls_dict.items()))])), key=len))
    maxline = len(max(
        [cmd.ljust(maxkey, ' ') + ": " + str(ctrls_dict.get(hdr).get(cmd)).strip('[]').replace('\'', '') for hdr in
         ctrls_dict for cmd in ctrls_dict.get(hdr)], key=len))
    for hdr in ctrls_dict:
        if hdr == header:
            rem = maxline - len(hdr)
            for x in range(rem + 1):
                if x == (int(-(-(rem / 2) // 1)) - 1):
                    print(hdr, end='')
                else:
                    print('_', end='') if x != rem else print('_')
            for cmd in ctrls_dict.get(hdr):
                print(cmd.ljust(maxkey, ' ') + ': ' + str(ctrls_dict.get(hdr).get(cmd)).strip('[]').replace('\'', ''))
        elif header is None:
            for cmd in ctrls_dict.get(hdr):
                if hdr != thdr:
                    thdr = hdr
                    rem = maxline - len(hdr)
                    for x in range(rem + 1):
                        if x == (int(-(-(rem / 2) // 1)) - 1):
                            print(hdr, end='')
                        else:
                            print('_', end='') if x != rem else print('_')
                print(cmd.ljust(maxkey, ' ') + ': ' + str(ctrls_dict.get(hdr).get(cmd)).strip('[]').replace('\'', ''))


def fetch_ctrls(q, command):
    for hdr in ctrls_dict:
        if ctrls_dict.get(hdr).get(command):
            return q.put(ctrls_dict.get(hdr).get(command))


def get_t2s_ctrls(q, header=None):
    fstrg = ''
    for hdr in ctrls_dict.keys():
        if header in hdr:
            commands = list(ctrls_dict.get(hdr).keys())
            # print(commands)
            for cmd in commands:
                ctrls = ctrls_dict.get(hdr).get(cmd)
                strg = 'To \'' + cmd + '\', press \''
                for x in range(len(ctrls)):
                    strg += ctrls[x]
                    if x < len(ctrls) - 1:
                        strg += '\', or \''
                    else:
                        strg += '\'. '
                fstrg += strg
    return q.put(fstrg)


def get_t2s_ctrls2(q):
    fstrg = ''
    for cmd in sctrls_dict:
        strg = 'To \''
        description = list(sctrls_dict.get(cmd).keys())[0]
        keywords = list(sctrls_dict.get(cmd).values())[0]
        strg += description + '\', say \''
        for x in range(len(keywords)):
            strg += keywords[x]
            if x < len(keywords) - 1:
                if keywords[x] == 'quit':
                    strg += '\', or, \''
                else:
                    strg += '\' '
            else:
                strg += '\'. '
        fstrg += strg
    return q.put(fstrg)


if __name__ == '__main__':
    import queue
    import threading
    q = queue.Queue()
    cmd = 'what color is this'
    # print_ctrls('[DEFAULT CONTROLS]')
    # print(q.get(get_t2s_ctrls(q, header='CUSTOM')))
    # print(q.get(threading.Thread(target=fetch_ctrls, args=('quit', q), daemon=True).start()))
    # print(q.get(threading.Thread(target=get_t2s_ctrls, args=(q, 'DEFAULT'), daemon=True).start()))
    # print(q.get(get_t2s_ctrls2(q)))
    print(q.get(fetch_ctrls(q, 'color check')))

    if all(word in cmd for word in q.get(fetch_ctrls(q, 'color check'))):
        print('ye')
    else:
        print('no')