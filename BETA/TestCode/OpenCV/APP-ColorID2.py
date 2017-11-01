from matplotlib import colors
import struct


def standard_colors():
    colors = [
        'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
        'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
        'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
        'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
        'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
        'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
        'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
        'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
        'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
        'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
        'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
        'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
        'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
        'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
        'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
        'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
        'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
        'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
        'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
        'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
        'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
        'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
        'WhiteSmoke', 'Yellow', 'YellowGreen'
    ]
    return colors


def rgb2name(carr, range):
    colors_rgb = []
    r = carr[0]
    g = carr[1]
    b = carr[2]
    l1 = []
    l2 = []
    l3 = []
    for key, value in colors.cnames.items():
        colors_rgb.append((key, struct.unpack('BBB', bytes.fromhex(value.replace('#', '')))))
    for val in colors_rgb:
        if r - range <= val[1][0] <= r + range:
            l1 += [val]
    # print("l1: " + str(l1))
    for val in l1:
        if g - range <= val[1][1] <= g + range:
            l2 += [val]
    # print("l2: " + str(l2))
    for val in l2:
        if b - range <= val[1][2] <= b + range:
            l3 += [val]
    # print("l3: " + str(l3))
    if len(l1) > 1:
        if len(l2) > 1:
            if len(l3) > 1:
                return rgb2name(carr, range - 1)
            elif len(l3) == 1:
                return l3[0][0]
            else:
                return rgb2name(carr, range - 1)
        elif len(l2) == 1:
            return l2[0][0]
        else:
            return rgb2name(carr, range - 1)
    elif len(l1) == 1:
        return l1[0][0]
    else:
        return []


# print(rgb2name([106, 0, 60], 10))
# print(rgb2name([232, 102,  96], 10))
print(rgb2name([255, 255, 255], 10))
for a in range(255):
    for b in range(255):
        for c in range(255):
            print([a, b, c], rgb2name([a, b, c], 10))
# print(int(round(106.46342213)))
