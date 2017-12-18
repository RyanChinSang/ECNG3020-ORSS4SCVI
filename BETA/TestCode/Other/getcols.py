import string


def getdupes(L):
    seen = set()
    seen2 = set()
    seen_add = seen.add
    seen2_add = seen2.add
    for item in L:
        if item in seen:
            seen2_add(item)
        else:
            seen_add(item)
    return list(seen2)


def remove_dupes(l):
    dupkeys = getdupes(lrgb)
    for rgb in dupkeys:
        t1 = [int(num) for num in rgb.replace(';', ' ').split()]
        t2 = []
        i = 0
        for num in t1:
            i += 1
            if num == 255:
                num -= 1
            else:
                num += 1
            if i < 3:
                t2 += [str(num) + ';']
            else:
                t2 += [str(num)]
            t2 = [''.join(t2)]
        lrgb[(len(lrgb) - 1) - lrgb[::-1].index(rgb)] = t2[0]
    if len(getdupes(lrgb)) != 0:
        remove_dupes(lrgb)


lnames = []
lrgb = []
file = open('colors.txt').read().split('\n')

for line in file:
    sline = line.split()
    if len(sline) >= 3:
        if len(sline) == 5:
            if sline[0][0] in list(string.ascii_letters):
                if sline[1][0] in list(string.ascii_letters):
                    if ',' in sline[0]:
                        sline = [sline[1], sline[2], sline[3], sline[4]]
                    else:
                        sline = [sline[0]+sline[1], sline[2], sline[3], sline[4]]
        if len(sline) == 4:
            if sline[0][0] in list(string.ascii_letters):
                if sline[1][0] in list(string.ascii_letters):
                    if ',' in sline[0]:
                        sline = [sline[1], sline[2], sline[3]]
                    else:
                        sline = [sline[0]+sline[1], sline[2], sline[3]]
                elif '[' in sline[1][0]:
                    sline = [sline[0], sline[2], sline[3]]
                elif len(sline[3]) == 3:
                    sline = [sline[0], sline[1], sline[2]]
        if len(sline) == 3:
            if sline[0][0] in list(string.ascii_letters):
                if ';' in sline[1]:
                    name = ''.join(' '+x if x.isupper() else x for x in sline[0]).strip()
                    h = name.rstrip('0123456789')
                    name = name[0:len(h)] + ' ' + name[len(h):]
                    lnames += [name.rstrip()]
                    lrgb += [sline[1]]


remove_dupes(lrgb[::-1])
col_dict = dict(zip(lrgb, lnames))

print(lnames)
print(lrgb)
print(len(lnames))
print(len(lrgb))
print(col_dict)
