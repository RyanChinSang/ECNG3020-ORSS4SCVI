import numpy as np

a = np.array([[200, 203, 191]])
# a = np.array([[]])
# b = np.array([199, 202, 190])
# c = np.array([203, 205, 196])
# d = a + b + c
x = 0
y = 0
a = np.append(a, [[199, 202, 190]], axis=0)
a = np.append(a, [[203, 205, 196]], axis=0)
print(a)
print(a.mean(axis=1))

for x in range(2):
    for y in range(2):
        if (x, y) == (0, 0):
            print('ye')
        else:
            print('ne')
# print(a.reshape(-1, 3))
# print(np.mean(a.reshape(-1, 3), axis=1))
# print(np.mean(a.reshape(-1, 3), axis=1))
# a = np.append(a, [[203, 205, 196]])

# print(a)
