import cv2
import collections
import numpy as np

'''
Documentation: https://web.njit.edu/~walsh/rgb.html
Reference: https://web.njit.edu/~kevin/rgb.pdf
'''

s = 5
colors_dict = collections.OrderedDict(
    [('84;84;84', 'Grey'), ('192;192;192', 'Silver'), ('190;190;190', 'grey'), ('211;211;211', 'Light Gray'),
     ('119;136;153', 'Light Slate Grey'), ('112;128;144', 'Slate Gray'), ('198;226;255', 'Slate Gray 1'),
     ('185;211;238', 'Slate Gray 2'), ('159;182;205', 'Slate Gray 3'), ('108;123;139', 'Slate Gray 4'),
     ('0;0;0', 'black'), ('1;1;1', 'grey 0'), ('3;3;3', 'grey 1'), ('5;5;5', 'grey 2'), ('8;8;8', 'grey 3'),
     ('10;10;10', 'grey 4'), ('13;13;13', 'grey 5'), ('15;15;15', 'grey 6'), ('18;18;18', 'grey 7'),
     ('20;20;20', 'grey 8'), ('23;23;23', 'grey 9'), ('26;26;26', 'grey 10'), ('28;28;28', 'grey 11'),
     ('31;31;31', 'grey 12'), ('33;33;33', 'grey 13'), ('36;36;36', 'grey 14'), ('38;38;38', 'grey 15'),
     ('41;41;41', 'grey 16'), ('43;43;43', 'grey 17'), ('46;46;46', 'grey 18'), ('48;48;48', 'grey 19'),
     ('51;51;51', 'grey 20'), ('54;54;54', 'grey 21'), ('56;56;56', 'grey 22'), ('59;59;59', 'grey 23'),
     ('61;61;61', 'grey 24'), ('64;64;64', 'grey 25'), ('66;66;66', 'grey 26'), ('69;69;69', 'grey 27'),
     ('71;71;71', 'grey 28'), ('74;74;74', 'grey 29'), ('77;77;77', 'grey 30'), ('79;79;79', 'grey 31'),
     ('82;82;82', 'grey 32'), ('85;85;85', 'grey 33'), ('87;87;87', 'grey 34'), ('89;89;89', 'grey 35'),
     ('92;92;92', 'grey 36'), ('94;94;94', 'grey 37'), ('97;97;97', 'grey 38'), ('99;99;99', 'grey 39'),
     ('102;102;102', 'grey 40'), ('105;105;105', 'Dim Grey'), ('107;107;107', 'grey 42'), ('110;110;110', 'grey 43'),
     ('112;112;112', 'grey 44'), ('115;115;115', 'grey 45'), ('117;117;117', 'grey 46'), ('120;120;120', 'grey 47'),
     ('122;122;122', 'grey 48'), ('125;125;125', 'grey 49'), ('127;127;127', 'grey 50'), ('130;130;130', 'grey 51'),
     ('133;133;133', 'grey 52'), ('135;135;135', 'grey 53'), ('138;138;138', 'grey 54'), ('140;140;140', 'grey 55'),
     ('143;143;143', 'grey 56'), ('145;145;145', 'grey 57'), ('148;148;148', 'grey 58'), ('150;150;150', 'grey 59'),
     ('153;153;153', 'grey 60'), ('156;156;156', 'grey 61'), ('158;158;158', 'grey 62'), ('161;161;161', 'grey 63'),
     ('163;163;163', 'grey 64'), ('166;166;166', 'grey 65'), ('168;168;168', 'grey 66'), ('171;171;171', 'grey 67'),
     ('173;173;173', 'grey 68'), ('176;176;176', 'grey 69'), ('179;179;179', 'grey 70'), ('181;181;181', 'grey 71'),
     ('184;184;184', 'grey 72'), ('186;186;186', 'grey 73'), ('189;189;189', 'grey 74'), ('191;191;191', 'grey 75'),
     ('194;194;194', 'grey 76'), ('196;196;196', 'grey 77'), ('199;199;199', 'grey 78'), ('201;201;201', 'grey 79'),
     ('204;204;204', 'grey 80'), ('207;207;207', 'grey 81'), ('209;209;209', 'grey 82'), ('212;212;212', 'grey 83'),
     ('214;214;214', 'grey 84'), ('217;217;217', 'grey 85'), ('219;219;219', 'grey 86'), ('222;222;222', 'grey 87'),
     ('224;224;224', 'grey 88'), ('227;227;227', 'grey 89'), ('229;229;229', 'grey 90'), ('232;232;232', 'grey 91'),
     ('235;235;235', 'grey 92'), ('237;237;237', 'grey 93'), ('240;240;240', 'grey 94'), ('242;242;242', 'grey 95'),
     ('245;245;245', 'grey 96'), ('247;247;247', 'grey 97'), ('250;250;250', 'grey 98'), ('252;252;252', 'grey 99'),
     ('255;255;255', 'White'), ('47;79;79', 'Dark Slate Grey'), ('86;86;86', 'Dim Grey'),
     ('205;205;205', 'Very Light Grey'), ('99;86;136', 'Free Speech Grey'), ('240;248;255', 'Alice Blue'),
     ('138;43;226', 'Blue Violet'), ('95;159;159', 'Cadet Blue'), ('95;158;160', 'Cadet Blue'),
     ('96;159;161', 'Cadet Blue'), ('152;245;255', 'Cadet Blue 1'), ('142;229;238', 'Cadet Blue 2'),
     ('122;197;205', 'Cadet Blue 3'), ('83;134;139', 'Cadet Blue 4'), ('66;66;111', 'Corn Flower Blue'),
     ('100;149;237', 'Cornflower Blue'), ('72;61;139', 'Dark Slate Blue'), ('0;206;209', 'Dark Turquoise'),
     ('0;191;255', 'Deep Sky Blue'), ('1;192;254', 'Deep Sky Blue 1'), ('0;178;238', 'Deep Sky Blue 2'),
     ('0;154;205', 'Deep Sky Blue 3'), ('0;104;139', 'Deep Sky Blue 4'), ('30;144;255', 'Dodger Blue'),
     ('31;145;254', 'Dodger Blue 1'), ('28;134;238', 'Dodger Blue 2'), ('24;116;205', 'Dodger Blue 3'),
     ('16;78;139', 'Dodger Blue 4'), ('173;216;230', 'Light Blue'), ('191;239;255', 'Light Blue 1'),
     ('178;223;238', 'Light Blue 2'), ('154;192;205', 'Light Blue 3'), ('104;131;139', 'Light Blue 4'),
     ('224;255;255', 'Light Cyan'), ('225;254;254', 'Light Cyan 1'), ('209;238;238', 'Light Cyan 2'),
     ('180;205;205', 'Light Cyan 3'), ('122;139;139', 'Light Cyan 4'), ('135;206;250', 'Light Sky Blue'),
     ('176;226;255', 'Light Sky Blue 1'), ('164;211;238', 'Light Sky Blue 2'), ('141;182;205', 'Light Sky Blue 3'),
     ('96;123;139', 'Light Sky Blue 4'), ('132;112;255', 'Light Slate Blue'), ('176;196;222', 'Light Steel Blue'),
     ('202;225;255', 'Light Steel Blue 1'), ('188;210;238', 'Light Steel Blue 2'),
     ('162;181;205', 'Light Steel Blue 3'), ('110;123;139', 'Light Steel Blue 4'), ('112;219;147', 'Aquamarine'),
     ('0;0;205', 'Medium Blue'), ('123;104;238', 'Medium Slate Blue'), ('72;209;204', 'Medium Turquoise'),
     ('25;25;112', 'Midnight Blue'), ('0;0;128', 'Navy Blue'), ('175;238;238', 'Pale Turquoise'),
     ('187;255;255', 'Pale Turquoise 1'), ('174;238;238', 'Pale Turquoise 2'), ('150;205;205', 'Pale Turquoise 3'),
     ('102;139;139', 'Pale Turquoise 4'), ('176;224;230', 'Powder Blue'), ('65;105;225', 'Royal Blue'),
     ('72;118;255', 'Royal Blue 1'), ('67;110;238', 'Royal Blue 2'), ('58;95;205', 'Royal Blue 3'),
     ('39;64;139', 'Royal Blue 4'), ('0;34;102', 'Royal Blue 5'), ('135;206;235', 'Sky Blue'),
     ('135;206;255', 'Sky Blue 1'), ('126;192;238', 'Sky Blue 2'), ('108;166;205', 'Sky Blue 3'),
     ('74;112;139', 'Sky Blue 4'), ('106;90;205', 'Slate Blue'), ('131;111;255', 'Slate Blue 1'),
     ('122;103;238', 'Slate Blue 2'), ('105;89;205', 'Slate Blue 3'), ('71;60;139', 'Slate Blue 4'),
     ('70;130;180', 'Steel Blue'), ('99;184;255', 'Steel Blue 1'), ('92;172;238', 'Steel Blue 2'),
     ('79;148;205', 'Steel Blue 3'), ('54;100;139', 'Steel Blue 4'), ('127;255;212', 'aquamarine'),
     ('128;254;213', 'aquamarine 1'), ('118;238;198', 'aquamarine 2'), ('102;205;170', 'Medium Aquamarine'),
     ('69;139;116', 'aquamarine 4'), ('240;255;255', 'azure'), ('241;254;254', 'azure 1'), ('224;238;238', 'azure 2'),
     ('193;205;205', 'azure 3'), ('131;139;139', 'azure 4'), ('0;0;255', 'blue'), ('1;1;254', 'blue 1'),
     ('0;0;238', 'blue 2'), ('1;1;206', 'blue 3'), ('0;0;139', 'blue 4'), ('0;255;255', 'aqua'), ('1;254;254', 'cyan'),
     ('2;255;255', 'cyan 1'), ('0;238;238', 'cyan 2'), ('0;205;205', 'cyan 3'), ('0;139;139', 'cyan 4'),
     ('1;1;129', 'navy'), ('0;128;128', 'teal'), ('64;224;208', 'turquoise'), ('0;245;255', 'turquoise 1'),
     ('0;229;238', 'turquoise 2'), ('0;197;205', 'turquoise 3'), ('0;134;139', 'turquoise 4'),
     ('48;80;80', 'Dark Slate Gray'), ('151;255;255', 'Dark Slate Gray 1'), ('141;238;238', 'Dark Slate Gray 2'),
     ('121;205;205', 'Dark Slate Gray 3'), ('82;139;139', 'Dark Slate Gray 4'), ('36;24;130', 'Dark Slate Blue'),
     ('112;147;219', 'Dark Turquoise'), ('127;0;255', 'Medium Slate Blue'), ('112;219;219', 'Medium Turquoise'),
     ('47;47;79', 'Midnight Blue'), ('35;35;142', 'Navy Blue'), ('77;77;255', 'Neon Blue'),
     ('0;0;156', 'New Midnight Blue'), ('89;89;171', 'Rich Blue'), ('50;153;204', 'Sky Blue'),
     ('0;127;255', 'Slate Blue'), ('56;176;222', 'Summer Sky'), ('3;180;200', 'Iris Blue'),
     ('65;86;197', 'Free Speech Blue'), ('188;143;143', 'Rosy Brown'), ('255;193;193', 'Rosy Brown 1'),
     ('238;180;180', 'Rosy Brown 2'), ('205;155;155', 'Rosy Brown 3'), ('139;105;105', 'Rosy Brown 4'),
     ('139;69;19', 'Saddle Brown'), ('244;164;96', 'Sandy Brown'), ('245;245;220', 'beige'), ('165;42;42', 'brown'),
     ('166;42;42', 'brown'), ('255;64;64', 'brown 1'), ('238;59;59', 'brown 2'), ('205;51;51', 'brown 3'),
     ('139;35;35', 'brown 4'), ('92;64;51', 'darkbrown'), ('222;184;135', 'burlywood'), ('255;211;155', 'burlywood 1'),
     ('238;197;145', 'burlywood 2'), ('205;170;125', 'burlywood 3'), ('139;115;85', 'burlywood 4'),
     ('92;51;23', "baker'schocolate"), ('210;105;30', 'chocolate'), ('255;127;36', 'chocolate 1'),
     ('238;118;33', 'chocolate 2'), ('205;102;29', 'chocolate 3'), ('140;70;20', 'chocolate 4'), ('205;133;63', 'peru'),
     ('210;180;140', 'tan'), ('255;165;79', 'tan 1'), ('238;154;73', 'tan 2'), ('206;134;64', 'tan 3'),
     ('139;90;43', 'tan 4'), ('151;105;79', 'Dark Tan'), ('133;94;66', 'Dark Wood'), ('133;99;99', 'Light Wood'),
     ('166;128;100', 'Medium Wood'), ('235;199;158', 'New Tan'), ('107;66;38', 'Semi- Sweet Chocolate'),
     ('142;107;35', 'Sienna'), ('219;147;112', 'Tan'), ('93;65;52', 'Very Dark Brown'), ('47;79;47', 'Dark Green'),
     ('0;100;0', 'Dark Green'), ('74;118;110', 'darkgreencopper'), ('189;183;107', 'Dark Khaki'),
     ('85;107;47', 'Dark Olive Green'), ('202;255;112', 'Dark Olive Green 1'), ('188;238;104', 'Dark Olive Green 2'),
     ('162;205;90', 'Dark Olive Green 3'), ('110;139;61', 'Dark Olive Green 4'), ('128;128;0', 'olive'),
     ('143;188;143', 'Dark Sea Green'), ('193;255;193', 'Dark Sea Green 1'), ('180;238;180', 'Dark Sea Green 2'),
     ('155;205;155', 'Dark Sea Green 3'), ('105;139;105', 'Dark Sea Green 4'), ('34;139;34', 'Forest Green'),
     ('173;255;47', 'Green Yellow'), ('124;252;0', 'Lawn Green'), ('32;178;170', 'Light Sea Green'),
     ('50;205;50', 'Lime Green'), ('60;179;113', 'Medium Sea Green'), ('0;250;154', 'Medium Spring Green'),
     ('245;255;250', 'Mint Cream'), ('107;142;35', 'Olive Drab'), ('192;255;62', 'Olive Drab 1'),
     ('179;238;58', 'Olive Drab 2'), ('154;205;50', 'Olive Drab 3'), ('105;139;34', 'Olive Drab 4'),
     ('152;251;152', 'Pale Green'), ('154;255;154', 'Pale Green 1'), ('144;238;144', 'Pale Green 2'),
     ('124;205;124', 'Pale Green 3'), ('84;139;84', 'Pale Green 4'), ('46;139;87', 'Sea Green 4'),
     ('84;255;159', 'Sea Green 1'), ('78;238;148', 'Sea Green 2'), ('67;205;128', 'Sea Green 3'),
     ('0;255;127', 'Spring Green'), ('1;254;128', 'Spring Green 1'), ('0;238;118', 'Spring Green 2'),
     ('0;205;102', 'Spring Green 3'), ('0;139;69', 'Spring Green 4'), ('155;206;51', 'Yellow Green'),
     ('127;255;0', 'chartreuse'), ('128;254;1', 'chartreuse 1'), ('118;238;0', 'chartreuse 2'),
     ('102;205;0', 'chartreuse 3'), ('69;139;0', 'chartreuse 4'), ('0;255;0', 'green'), ('0;128;0', 'green'),
     ('1;254;1', 'lime'), ('2;255;2', 'green 1'), ('0;238;0', 'green 2'), ('0;205;0', 'green 3'),
     ('0;139;0', 'green 4'), ('240;230;140', 'khaki'), ('255;246;143', 'khaki 1'), ('238;230;133', 'khaki 2'),
     ('205;198;115', 'khaki 3'), ('139;134;78', 'khaki 4'), ('79;79;47', 'Dark Olive Green'),
     ('35;142;35', 'Medium Aquamarine'), ('219;219;112', 'Medium Forest Green'), ('66;111;66', 'Medium Sea Green'),
     ('129;255;2', 'Medium Spring Green'), ('144;189;144', 'Pale Green'), ('35;142;104', 'Sea Green'),
     ('2;255;129', 'Spring Green'), ('9;249;17', 'Free Speech Green'), ('2;157;116', 'Aquamarine'),
     ('255;140;0', 'Dark Orange'), ('255;127;0', 'Dark Orange 1'), ('238;118;0', 'Dark Orange 2'),
     ('205;102;0', 'Dark Orange 3'), ('139;69;0', 'Dark Orange 4'), ('233;150;122', 'Dark Salmon'),
     ('240;128;128', 'Light Coral'), ('255;160;122', 'Light Salmon'), ('254;161;123', 'Light Salmon 1'),
     ('238;149;114', 'Light Salmon 2'), ('205;129;98', 'Light Salmon 3'), ('139;87;66', 'Light Salmon 4'),
     ('255;218;185', 'Peach Puff'), ('254;219;186', 'Peach Puff 1'), ('238;203;173', 'Peach Puff 2'),
     ('205;175;149', 'Peach Puff 3'), ('139;119;101', 'Peach Puff 4'), ('255;228;196', 'bisque'),
     ('254;229;197', 'bisque 1'), ('238;213;183', 'bisque 2'), ('205;183;158', 'bisque 3'), ('139;125;107', 'bisque 4'),
     ('254;128;1', 'coral'), ('255;127;80', 'coral'), ('255;114;86', 'coral 1'), ('238;106;80', 'coral 2'),
     ('205;91;69', 'coral 3'), ('139;62;47', 'coral 4'), ('240;255;240', 'honeydew'), ('241;254;241', 'honeydew 1'),
     ('224;238;224', 'honeydew 2'), ('193;205;193', 'honeydew 3'), ('131;139;131', 'honeydew 4'),
     ('255;165;0', 'orange'), ('254;166;1', 'orange 1'), ('238;154;0', 'orange 2'), ('205;133;0', 'orange 3'),
     ('139;90;0', 'orange 4'), ('250;128;114', 'salmon'), ('255;140;105', 'salmon 1'), ('238;130;98', 'salmon 2'),
     ('205;112;84', 'salmon 3'), ('139;76;57', 'salmon 4'), ('160;82;45', 'sienna'), ('255;130;71', 'sienna 1'),
     ('238;121;66', 'sienna 2'), ('205;104;57', 'sienna 3'), ('139;71;38', 'sienna 4'),
     ('142;35;35', 'Mandarian Orange'), ('255;129;2', 'Orange'), ('255;36;0', 'Orange Red'),
     ('255;20;147', 'Deep Pink'), ('254;21;148', 'Deep Pink 1'), ('238;18;137', 'Deep Pink 2'),
     ('205;16;118', 'Deep Pink 3'), ('139;10;80', 'Deep Pink 4'), ('255;105;180', 'Hot Pink'),
     ('255;110;180', 'Hot Pink 1'), ('238;106;167', 'Hot Pink 2'), ('205;96;144', 'Hot Pink 3'),
     ('139;58;98', 'Hot Pink 4'), ('205;92;92', 'Indian Red'), ('255;106;106', 'Indian Red 1'),
     ('238;99;99', 'Indian Red 2'), ('205;85;85', 'Indian Red 3'), ('139;58;58', 'Indian Red 4'),
     ('255;182;193', 'Light Pink'), ('255;174;185', 'Light Pink 1'), ('238;162;173', 'Light Pink 2'),
     ('205;140;149', 'Light Pink 3'), ('139;95;101', 'Light Pink 4'), ('199;21;133', 'Medium Violet Red'),
     ('255;228;225', 'Misty Rose'), ('254;229;226', 'Misty Rose 1'), ('238;213;210', 'Misty Rose 2'),
     ('205;183;181', 'Misty Rose 3'), ('139;125;123', 'Misty Rose 4'), ('255;69;0', 'Orange Red'),
     ('254;70;1', 'Orange Red 1'), ('238;64;0', 'Orange Red 2'), ('205;55;0', 'Orange Red 3'),
     ('139;37;0', 'Orange Red 4'), ('219;112;147', 'Pale Violet Red'), ('255;130;171', 'Pale Violet Red 1'),
     ('238;121;159', 'Pale Violet Red 2'), ('205;104;137', 'Pale Violet Red 3'), ('139;71;93', 'Pale Violet Red 4'),
     ('208;32;144', 'Violet Red'), ('255;62;150', 'Violet Red 1'), ('238;58;140', 'Violet Red 2'),
     ('205;50;120', 'Violet Red 3'), ('139;34;82', 'Violet Red 4'), ('178;34;34', 'firebrick'),
     ('255;48;48', 'firebrick 1'), ('238;44;44', 'firebrick 2'), ('205;38;38', 'firebrick 3'),
     ('139;26;26', 'firebrick 4'), ('255;192;203', 'pink'), ('255;181;197', 'pink 1'), ('238;169;184', 'pink 2'),
     ('205;145;158', 'pink 3'), ('139;99;108', 'pink 4'), ('245;204;176', 'Flesh'), ('209;146;117', 'Feldspar'),
     ('255;0;0', 'red'), ('254;1;1', 'red 1'), ('238;0;0', 'red 2'), ('205;0;0', 'red 3'), ('139;0;0', 'red 4'),
     ('255;99;71', 'tomato'), ('254;100;72', 'tomato 1'), ('238;92;66', 'tomato 2'), ('205;79;57', 'tomato 3'),
     ('139;54;38', 'tomato 4'), ('134;100;100', 'Dusty Rose'), ('143;36;36', 'Firebrick'),
     ('246;205;177', 'Indian Red'), ('189;144;144', 'Pink'), ('111;66;66', 'Salmon'), ('140;23;23', 'Scarlet'),
     ('255;28;174', 'Spicy Pink'), ('227;91;216', 'Free Speech Magenta'), ('192;0;0', 'Free Speech Red'),
     ('153;50;204', 'Dark Orchid'), ('191;62;255', 'Dark Orchid 1'), ('178;58;238', 'Dark Orchid 2'),
     ('154;50;205', 'Dark Orchid 3'), ('104;34;139', 'Dark Orchid 4'), ('148;0;211', 'Dark Violet'),
     ('255;240;245', 'Lavender Blush'), ('254;241;246', 'Lavender Blush 1'), ('238;224;229', 'Lavender Blush 2'),
     ('205;193;197', 'Lavender Blush 3'), ('139;131;134', 'Lavender Blush 4'), ('186;85;211', 'Medium Orchid'),
     ('224;102;255', 'Medium Orchid 1'), ('209;95;238', 'Medium Orchid 2'), ('180;82;205', 'Medium Orchid 3'),
     ('122;55;139', 'Medium Orchid 4'), ('147;112;219', 'Medium Purple'), ('148;113;220', 'Medium Orchid'),
     ('171;130;255', 'Medium Purple 1'), ('153;50;205', 'Dark Orchid'), ('159;121;238', 'Medium Purple 2'),
     ('137;104;205', 'Medium Purple 3'), ('93;71;139', 'Medium Purple 4'), ('230;230;250', 'lavender'),
     ('255;0;255', 'magenta'), ('254;1;254', 'fuchsia'), ('255;2;255', 'magenta 1'), ('238;0;238', 'magenta 2'),
     ('205;0;205', 'magenta 3'), ('139;0;139', 'magenta 4'), ('176;48;96', 'maroon'), ('255;52;179', 'maroon 1'),
     ('238;48;167', 'maroon 2'), ('205;41;144', 'maroon 3'), ('139;28;98', 'maroon 4'), ('218;112;214', 'orchid'),
     ('219;112;219', 'Orchid'), ('255;131;250', 'orchid 1'), ('238;122;233', 'orchid 2'), ('205;105;201', 'orchid 3'),
     ('139;71;137', 'orchid 4'), ('221;160;221', 'plum'), ('255;187;255', 'plum 1'), ('238;174;238', 'plum 2'),
     ('205;150;205', 'plum 3'), ('139;102;139', 'plum 4'), ('160;32;240', 'purple'), ('128;0;128', 'purple'),
     ('155;48;255', 'purple 1'), ('145;44;238', 'purple 2'), ('125;38;205', 'purple 3'), ('85;26;139', 'purple 4'),
     ('216;191;216', 'thistle'), ('255;225;255', 'thistle 1'), ('238;210;238', 'thistle 2'),
     ('205;181;205', 'thistle 3'), ('139;123;139', 'thistle 4'), ('238;130;238', 'violet'),
     ('159;95;159', 'violetblue'), ('135;31;120', 'Dark Purple'), ('128;0;0', 'Maroon'),
     ('220;113;148', 'Medium Violet Red'), ('255;110;199', 'Neon Pink'), ('234;173;234', 'Plum'),
     ('217;192;217', 'Thistle'), ('173;234;234', 'Turquoise'), ('79;47;79', 'Violet'), ('204;50;153', 'Violet Red'),
     ('250;235;215', 'Antique White'), ('255;239;219', 'Antique White 1'), ('238;223;204', 'Antique White 2'),
     ('205;192;176', 'Antique White 3'), ('139;131;120', 'Antique White 4'), ('255;250;240', 'Floral White'),
     ('248;248;255', 'Ghost White'), ('255;222;173', 'Navajo White'), ('254;223;174', 'Navajo White 1'),
     ('238;207;161', 'Navajo White 2'), ('205;179;139', 'Navajo White 3'), ('139;121;94', 'Navajo White 4'),
     ('253;245;230', 'Old Lace'), ('246;246;246', 'White Smoke'), ('220;220;220', 'gainsboro'),
     ('255;255;240', 'ivory'), ('254;254;241', 'ivory 1'), ('238;238;224', 'ivory 2'), ('205;205;193', 'ivory 3'),
     ('139;139;131', 'ivory 4'), ('250;240;230', 'linen'), ('255;245;238', 'seashell'), ('254;246;239', 'seashell 1'),
     ('238;229;222', 'seashell 2'), ('205;197;191', 'seashell 3'), ('139;134;130', 'seashell 4'),
     ('255;250;250', 'snow'), ('254;251;251', 'snow 1'), ('238;233;233', 'snow 2'), ('205;201;201', 'snow 3'),
     ('139;137;137', 'snow 4'), ('245;222;179', 'wheat'), ('255;231;186', 'wheat 1'), ('238;216;174', 'wheat 2'),
     ('205;186;150', 'wheat 3'), ('139;126;102', 'wheat 4'), ('254;254;254', 'white'), ('217;217;243', 'Quartz'),
     ('216;216;191', 'Wheat'), ('255;235;205', 'Blanched Almond'), ('184;134;11', 'Dark Goldenrod'),
     ('255;185;15', 'Dark Goldenrod 1'), ('238;173;14', 'Dark Goldenrod 2'), ('205;149;12', 'Dark Goldenrod 3'),
     ('139;101;8', 'Dark Goldenrod 4'), ('255;250;205', 'Lemon Chiffon'), ('254;251;206', 'Lemon Chiffon 1'),
     ('238;233;191', 'Lemon Chiffon 2'), ('205;201;165', 'Lemon Chiffon 3'), ('139;137;112', 'Lemon Chiffon 4'),
     ('238;221;130', 'Light Goldenrod'), ('255;236;139', 'Light Goldenrod 1'), ('238;220;130', 'Light Goldenrod 2'),
     ('205;190;112', 'Light Goldenrod 3'), ('139;129;76', 'Light Goldenrod 4'),
     ('250;250;210', 'Light Goldenrod Yellow'), ('255;255;224', 'Light Yellow'), ('254;254;225', 'Light Yellow 1'),
     ('238;238;209', 'Light Yellow 2'), ('205;205;180', 'Light Yellow 3'), ('139;139;122', 'Light Yellow 4'),
     ('238;232;170', 'Pale Goldenrod'), ('255;239;213', 'Papaya Whip'), ('255;248;220', 'cornsilk'),
     ('254;249;221', 'cornsilk 1'), ('238;232;205', 'cornsilk 2'), ('205;200;177', 'cornsilk 3'),
     ('139;136;120', 'cornsilk 4'), ('218;165;32', 'goldenrod'), ('255;193;37', 'goldenrod 1'),
     ('238;180;34', 'goldenrod 2'), ('205;155;29', 'goldenrod 3'), ('139;105;20', 'goldenrod 4'),
     ('255;228;181', 'moccasin'), ('255;255;0', 'yellow'), ('254;254;1', 'yellow 1'), ('238;238;0', 'yellow 2'),
     ('205;205;0', 'yellow 3'), ('139;139;0', 'yellow 4'), ('255;215;0', 'gold'), ('254;216;1', 'gold 1'),
     ('238;201;0', 'gold 2'), ('205;173;0', 'gold 3'), ('139;117;0', 'gold 4'), ('220;220;113', 'Goldenrod'),
     ('234;234;174', 'Medium Goldenrod'), ('153;204;50', 'Yellow Green')])


def color_id(q, frame, size, mode=None):
    frame = cv2.blur(cv2.GaussianBlur(frame, (s, s), 0), (s, s))
    frame_height, frame_width = frame.shape[:2]
    rgb = np.array([])
    for x in range(size * 2):
        for y in range(size * 2):
            if (x, y) == (0, 0):
                rgb = np.array([frame[int((frame_height / 2) - size) + x][
                                    int((frame_width / 2) - size) + y]])
            else:
                rgb = np.append(rgb, [frame[int((frame_height / 2) - size) + x][
                                          int((frame_width / 2) - size) + y]], axis=0)
    requested_color = rgb.mean(axis=0)
    min_dif = 16581375  # Maximum possible difference of (255)^3
    closest_color = None
    for color in colors_dict.keys():
        r_c, g_c, b_c = color.split(';')
        dif_val = ((int(b_c) - requested_color[0]) ** 2) + ((int(g_c) - requested_color[1]) ** 2) + \
                  ((int(r_c) - requested_color[2]) ** 2)
        if min_dif > dif_val:
            min_dif = dif_val
            closest_color = colors_dict[color]
    if mode is None:
        return q.put(closest_color)
    else:
        return q.put(color_catg(list(colors_dict.values()).index(closest_color)))


def color_catg(color_index):
    if 0 <= color_index <= 9:
        return 'grey'
    elif 10 <= color_index <= 51:
        return 'black'
    elif 52 <= color_index <= 83:
        return 'grey'
    elif 84 <= color_index <= 115:
        return 'white'
    elif 116 <= color_index <= 239:
        return 'blue'
    elif 240 <= color_index <= 280:
        return 'brown'
    elif 281 <= color_index <= 350:
        return 'green'
    elif 351 <= color_index <= 401:
        return 'orange'
    elif 402 <= color_index <= 473:
        return 'red'
    elif 474 <= color_index <= 541:
        return 'violet'
    elif 542 <= color_index <= 580:
        return 'white'
    elif 581 <= color_index <= 628:
        return 'yellow'
    else:
        return 'error'


if __name__ == '__main__':
    print(list(colors_dict.values())[int(69)])
    print(list(colors_dict.values()).index('Alice Blue'))
