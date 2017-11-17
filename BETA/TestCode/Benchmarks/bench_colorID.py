import webcolors
import timeit
import numpy as np

# print(webcolors.css3_hex_to_names.__str__())  # {'#f0f8ff': 'aliceblue'}
# for key, name in webcolors.css3_hex_to_names.items():
#     # r, g, b = webcolors.hex_to_rgb(key)
#     # print("'" + str([r, g, b]) + "': '" + str(name) + "', ")
#     print("'" + key + "': '" + name + "', ")


colors = {'[240, 248, 255]': 'aliceblue',
          '[250, 235, 215]': 'antiquewhite',
          '[0, 255, 255]': 'cyan',
          '[127, 255, 212]': 'aquamarine',
          '[240, 255, 255]': 'azure',
          '[245, 245, 220]': 'beige',
          '[255, 228, 196]': 'bisque',
          '[0, 0, 0]': 'black',
          '[255, 235, 205]': 'blanchedalmond',
          '[0, 0, 255]': 'blue',
          '[138, 43, 226]': 'blueviolet',
          '[165, 42, 42]': 'brown',
          '[222, 184, 135]': 'burlywood',
          '[95, 158, 160]': 'cadetblue',
          '[127, 255, 0]': 'chartreuse',
          '[210, 105, 30]': 'chocolate',
          '[255, 127, 80]': 'coral',
          '[100, 149, 237]': 'cornflowerblue',
          '[255, 248, 220]': 'cornsilk',
          '[220, 20, 60]': 'crimson',
          '[0, 0, 139]': 'darkblue',
          '[0, 139, 139]': 'darkcyan',
          '[184, 134, 11]': 'darkgoldenrod',
          '[169, 169, 169]': 'darkgrey',
          '[0, 100, 0]': 'darkgreen',
          '[189, 183, 107]': 'darkkhaki',
          '[139, 0, 139]': 'darkmagenta',
          '[85, 107, 47]': 'darkolivegreen',
          '[255, 140, 0]': 'darkorange',
          '[153, 50, 204]': 'darkorchid',
          '[139, 0, 0]': 'darkred',
          '[233, 150, 122]': 'darksalmon',
          '[143, 188, 143]': 'darkseagreen',
          '[72, 61, 139]': 'darkslateblue',
          '[47, 79, 79]': 'darkslategrey',
          '[0, 206, 209]': 'darkturquoise',
          '[148, 0, 211]': 'darkviolet',
          '[255, 20, 147]': 'deeppink',
          '[0, 191, 255]': 'deepskyblue',
          '[105, 105, 105]': 'dimgrey',
          '[30, 144, 255]': 'dodgerblue',
          '[178, 34, 34]': 'firebrick',
          '[255, 250, 240]': 'floralwhite',
          '[34, 139, 34]': 'forestgreen',
          '[255, 0, 255]': 'magenta',
          '[220, 220, 220]': 'gainsboro',
          '[248, 248, 255]': 'ghostwhite',
          '[255, 215, 0]': 'gold',
          '[218, 165, 32]': 'goldenrod',
          '[128, 128, 128]': 'grey',
          '[0, 128, 0]': 'green',
          '[173, 255, 47]': 'greenyellow',
          '[240, 255, 240]': 'honeydew',
          '[255, 105, 180]': 'hotpink',
          '[205, 92, 92]': 'indianred',
          '[75, 0, 130]': 'indigo',
          '[255, 255, 240]': 'ivory',
          '[240, 230, 140]': 'khaki',
          '[230, 230, 250]': 'lavender',
          '[255, 240, 245]': 'lavenderblush',
          '[124, 252, 0]': 'lawngreen',
          '[255, 250, 205]': 'lemonchiffon',
          '[173, 216, 230]': 'lightblue',
          '[240, 128, 128]': 'lightcoral',
          '[224, 255, 255]': 'lightcyan',
          '[250, 250, 210]': 'lightgoldenrodyellow',
          '[211, 211, 211]': 'lightgrey',
          '[144, 238, 144]': 'lightgreen',
          '[255, 182, 193]': 'lightpink',
          '[255, 160, 122]': 'lightsalmon',
          '[32, 178, 170]': 'lightseagreen',
          '[135, 206, 250]': 'lightskyblue',
          '[119, 136, 153]': 'lightslategrey',
          '[176, 196, 222]': 'lightsteelblue',
          '[255, 255, 224]': 'lightyellow',
          '[0, 255, 0]': 'lime',
          '[50, 205, 50]': 'limegreen',
          '[250, 240, 230]': 'linen',
          '[128, 0, 0]': 'maroon',
          '[102, 205, 170]': 'mediumaquamarine',
          '[0, 0, 205]': 'mediumblue',
          '[186, 85, 211]': 'mediumorchid',
          '[147, 112, 219]': 'mediumpurple',
          '[60, 179, 113]': 'mediumseagreen',
          '[123, 104, 238]': 'mediumslateblue',
          '[0, 250, 154]': 'mediumspringgreen',
          '[72, 209, 204]': 'mediumturquoise',
          '[199, 21, 133]': 'mediumvioletred',
          '[25, 25, 112]': 'midnightblue',
          '[245, 255, 250]': 'mintcream',
          '[255, 228, 225]': 'mistyrose',
          '[255, 228, 181]': 'moccasin',
          '[255, 222, 173]': 'navajowhite',
          '[0, 0, 128]': 'navy',
          '[253, 245, 230]': 'oldlace',
          '[128, 128, 0]': 'olive',
          '[107, 142, 35]': 'olivedrab',
          '[255, 165, 0]': 'orange',
          '[255, 69, 0]': 'orangered',
          '[218, 112, 214]': 'orchid',
          '[238, 232, 170]': 'palegoldenrod',
          '[152, 251, 152]': 'palegreen',
          '[175, 238, 238]': 'paleturquoise',
          '[219, 112, 147]': 'palevioletred',
          '[255, 239, 213]': 'papayawhip',
          '[255, 218, 185]': 'peachpuff',
          '[205, 133, 63]': 'peru',
          '[255, 192, 203]': 'pink',
          '[221, 160, 221]': 'plum',
          '[176, 224, 230]': 'powderblue',
          '[128, 0, 128]': 'purple',
          '[255, 0, 0]': 'red',
          '[188, 143, 143]': 'rosybrown',
          '[65, 105, 225]': 'royalblue',
          '[139, 69, 19]': 'saddlebrown',
          '[250, 128, 114]': 'salmon',
          '[244, 164, 96]': 'sandybrown',
          '[46, 139, 87]': 'seagreen',
          '[255, 245, 238]': 'seashell',
          '[160, 82, 45]': 'sienna',
          '[192, 192, 192]': 'silver',
          '[135, 206, 235]': 'skyblue',
          '[106, 90, 205]': 'slateblue',
          '[112, 128, 144]': 'slategrey',
          '[255, 250, 250]': 'snow',
          '[0, 255, 127]': 'springgreen',
          '[70, 130, 180]': 'steelblue',
          '[210, 180, 140]': 'tan',
          '[0, 128, 128]': 'teal',
          '[216, 191, 216]': 'thistle',
          '[255, 99, 71]': 'tomato',
          '[64, 224, 208]': 'turquoise',
          '[238, 130, 238]': 'violet',
          '[245, 222, 179]': 'wheat',
          '[255, 255, 255]': 'white',
          '[245, 245, 245]': 'whitesmoke',
          '[255, 255, 0]': 'yellow',
          '[154, 205, 50]': 'yellowgreen'}

hcolors = {'#f0f8ff': 'aliceblue',
           '#faebd7': 'antiquewhite',
           '#00ffff': 'cyan',
           '#7fffd4': 'aquamarine',
           '#f0ffff': 'azure',
           '#f5f5dc': 'beige',
           '#ffe4c4': 'bisque',
           '#000000': 'black',
           '#ffebcd': 'blanchedalmond',
           '#0000ff': 'blue',
           '#8a2be2': 'blueviolet',
           '#a52a2a': 'brown',
           '#deb887': 'burlywood',
           '#5f9ea0': 'cadetblue',
           '#7fff00': 'chartreuse',
           '#d2691e': 'chocolate',
           '#ff7f50': 'coral',
           '#6495ed': 'cornflowerblue',
           '#fff8dc': 'cornsilk',
           '#dc143c': 'crimson',
           '#00008b': 'darkblue',
           '#008b8b': 'darkcyan',
           '#b8860b': 'darkgoldenrod',
           '#a9a9a9': 'darkgrey',
           '#006400': 'darkgreen',
           '#bdb76b': 'darkkhaki',
           '#8b008b': 'darkmagenta',
           '#556b2f': 'darkolivegreen',
           '#ff8c00': 'darkorange',
           '#9932cc': 'darkorchid',
           '#8b0000': 'darkred',
           '#e9967a': 'darksalmon',
           '#8fbc8f': 'darkseagreen',
           '#483d8b': 'darkslateblue',
           '#2f4f4f': 'darkslategrey',
           '#00ced1': 'darkturquoise',
           '#9400d3': 'darkviolet',
           '#ff1493': 'deeppink',
           '#00bfff': 'deepskyblue',
           '#696969': 'dimgrey',
           '#1e90ff': 'dodgerblue',
           '#b22222': 'firebrick',
           '#fffaf0': 'floralwhite',
           '#228b22': 'forestgreen',
           '#ff00ff': 'magenta',
           '#dcdcdc': 'gainsboro',
           '#f8f8ff': 'ghostwhite',
           '#ffd700': 'gold',
           '#daa520': 'goldenrod',
           '#808080': 'grey',
           '#008000': 'green',
           '#adff2f': 'greenyellow',
           '#f0fff0': 'honeydew',
           '#ff69b4': 'hotpink',
           '#cd5c5c': 'indianred',
           '#4b0082': 'indigo',
           '#fffff0': 'ivory',
           '#f0e68c': 'khaki',
           '#e6e6fa': 'lavender',
           '#fff0f5': 'lavenderblush',
           '#7cfc00': 'lawngreen',
           '#fffacd': 'lemonchiffon',
           '#add8e6': 'lightblue',
           '#f08080': 'lightcoral',
           '#e0ffff': 'lightcyan',
           '#fafad2': 'lightgoldenrodyellow',
           '#d3d3d3': 'lightgrey',
           '#90ee90': 'lightgreen',
           '#ffb6c1': 'lightpink',
           '#ffa07a': 'lightsalmon',
           '#20b2aa': 'lightseagreen',
           '#87cefa': 'lightskyblue',
           '#778899': 'lightslategrey',
           '#b0c4de': 'lightsteelblue',
           '#ffffe0': 'lightyellow',
           '#00ff00': 'lime',
           '#32cd32': 'limegreen',
           '#faf0e6': 'linen',
           '#800000': 'maroon',
           '#66cdaa': 'mediumaquamarine',
           '#0000cd': 'mediumblue',
           '#ba55d3': 'mediumorchid',
           '#9370db': 'mediumpurple',
           '#3cb371': 'mediumseagreen',
           '#7b68ee': 'mediumslateblue',
           '#00fa9a': 'mediumspringgreen',
           '#48d1cc': 'mediumturquoise',
           '#c71585': 'mediumvioletred',
           '#191970': 'midnightblue',
           '#f5fffa': 'mintcream',
           '#ffe4e1': 'mistyrose',
           '#ffe4b5': 'moccasin',
           '#ffdead': 'navajowhite',
           '#000080': 'navy',
           '#fdf5e6': 'oldlace',
           '#808000': 'olive',
           '#6b8e23': 'olivedrab',
           '#ffa500': 'orange',
           '#ff4500': 'orangered',
           '#da70d6': 'orchid',
           '#eee8aa': 'palegoldenrod',
           '#98fb98': 'palegreen',
           '#afeeee': 'paleturquoise',
           '#db7093': 'palevioletred',
           '#ffefd5': 'papayawhip',
           '#ffdab9': 'peachpuff',
           '#cd853f': 'peru',
           '#ffc0cb': 'pink',
           '#dda0dd': 'plum',
           '#b0e0e6': 'powderblue',
           '#800080': 'purple',
           '#ff0000': 'red',
           '#bc8f8f': 'rosybrown',
           '#4169e1': 'royalblue',
           '#8b4513': 'saddlebrown',
           '#fa8072': 'salmon',
           '#f4a460': 'sandybrown',
           '#2e8b57': 'seagreen',
           '#fff5ee': 'seashell',
           '#a0522d': 'sienna',
           '#c0c0c0': 'silver',
           '#87ceeb': 'skyblue',
           '#6a5acd': 'slateblue',
           '#708090': 'slategrey',
           '#fffafa': 'snow',
           '#00ff7f': 'springgreen',
           '#4682b4': 'steelblue',
           '#d2b48c': 'tan',
           '#008080': 'teal',
           '#d8bfd8': 'thistle',
           '#ff6347': 'tomato',
           '#40e0d0': 'turquoise',
           '#ee82ee': 'violet',
           '#f5deb3': 'wheat',
           '#ffffff': 'white',
           '#f5f5f5': 'whitesmoke',
           '#ffff00': 'yellow',
           '#9acd32': 'yellowgreen'}


def avg_color():
    rgb = np.array([])
    requested_color = rgb.mean(axis=0)
    min_colors = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[2]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[0]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]


def closest_color5(requested_color):
    min_colors = {}
    for key, name in colors.items():
        r_c, g_c, b_c = int(key[1:key.find(',')]), int(key[key.find(',') + 2:][:key[key.find(',') + 2:].find(',')]), \
                        int(key[key.find(',') + 1:][key[key.find(',') + 1:].find(',') + 2:].replace(']', ''))
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]


def closest_color3(requested_color):
    min_colors = {}
    for color in colors.keys():
        r_c, g_c, b_c = color.replace(' ', '').strip("[]").split(",")
        rd = (int(r_c) - requested_color[0]) ** 2
        gd = (int(g_c) - requested_color[1]) ** 2
        bd = (int(b_c) - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = colors.get(color)
    return min_colors[min(min_colors.keys())]


def closest_color2(requested_color):
    min_colors = {}
    for color in colors.keys():
        r_c, g_c, b_c = color.replace("[", '').replace(']', '').replace(' ', '').split(",")
        rd = (int(r_c) - requested_color[0]) ** 2
        gd = (int(g_c) - requested_color[1]) ** 2
        bd = (int(b_c) - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = colors.get(color)
    return min_colors[min(min_colors.keys())]


def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]


def closest_color4(requested_color):
    min_colors = {}
    for key, name in hcolors.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]


def closest_color6(requested_color):
    min_dif = 16581375
    closest_color = None
    for color in colors.keys():
        r_c, g_c, b_c = color.replace(' ', '').strip("[]").split(",")
        dif_val = ((int(r_c) - requested_color[0]) ** 2) + ((int(g_c) - requested_color[1]) ** 2) +\
                  ((int(b_c) - requested_color[2]) ** 2)
        if min_dif > dif_val:
            min_dif = dif_val
            closest_color = colors.get(color)
    return closest_color


def closest_color7(requested_color):
    min_dif = 16581375  # Maximum possible difference of (255)^3
    closest_color = None
    for color in colors.keys():
        r_c, g_c, b_c = color.replace(' ', '').strip("[]").split(",")
        dif_val = ((int(r_c) - requested_color[0]) ** 2) + ((int(g_c) - requested_color[1]) ** 2) +\
                  ((int(b_c) - requested_color[2]) ** 2)
        if min_dif > dif_val:
            min_dif = dif_val
            closest_color = colors[color]
    return closest_color


iterations = 1000
orig = timeit.Timer(stmt="closest_color([240, 135, 10])", setup="from __main__ import closest_color")
repl = timeit.Timer(stmt="closest_color2([240, 135, 10])", setup="from __main__ import closest_color2")
strp = timeit.Timer(stmt="closest_color3([240, 135, 10])", setup="from __main__ import closest_color3")
hori = timeit.Timer(stmt="closest_color4([240, 135, 10])", setup="from __main__ import closest_color4")
find = timeit.Timer(stmt="closest_color5([240, 135, 10])", setup="from __main__ import closest_color5")
lmin = timeit.Timer(stmt="closest_color6([240, 135, 10])", setup="from __main__ import closest_color6")  # Uses new algo
lmi2 = timeit.Timer(stmt="closest_color7([240, 135, 10])", setup="from __main__ import closest_color7")  # Uses []-get()

orig.val = orig.timeit(iterations)
repl.val = repl.timeit(iterations)
strp.val = strp.timeit(iterations)
hori.val = hori.timeit(iterations)
find.val = find.timeit(iterations)
lmin.val = lmin.timeit(iterations)
lmi2.val = lmi2.timeit(iterations)

min_val = min([orig.val, repl.val, strp.val, hori.val, find.val, lmin.val, lmi2.val])

print('orig %0.12f (%0.2f%% as fast)' % (orig.val, (100 * min_val / orig.val), ))
print('repl %0.12f (%0.2f%% as fast)' % (repl.val, (100 * min_val / repl.val), ))
print('strp %0.12f (%0.2f%% as fast)' % (strp.val, (100 * min_val / strp.val), ))
print('hori %0.12f (%0.2f%% as fast)' % (hori.val, (100 * min_val / hori.val), ))
print('find %0.12f (%0.2f%% as fast)' % (find.val, (100 * min_val / find.val), ))
print('lmin %0.12f (%0.2f%% as fast)' % (lmin.val, (100 * min_val / lmin.val), ))
print('lmi2 %0.12f (%0.2f%% as fast)' % (lmi2.val, (100 * min_val / lmi2.val), ))

# COMPARE
# orig 0.427860205147 (78.52% as fast)
# repl 0.404157705357 (83.13% as fast)
# strp 0.382612635960 (87.81% as fast)
# hori 0.427458032626 (78.60% as fast)
# find 0.519428330328 (64.68% as fast)
# lmin 0.340100472019 (98.79% as fast)
# lmi2 0.335972080220 (100.00% as fast)
