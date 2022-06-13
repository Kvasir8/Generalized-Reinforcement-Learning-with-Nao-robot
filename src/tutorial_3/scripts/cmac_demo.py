import pandas as pd
import numpy as np
import math
resolution = 50
n_a = 3  # receptive field size
n_x = 2
n_y = 2
n_w = 1000
miu = []
lr = 0.01

df = pd.read_csv('samples.csv')  # you need change the address first
print(df[0:5])
print(df.columns)
d = list(np.empty([2, n_a]))
# d = [[]]
# displacement
d[0][0] = 2
d[0][1] = 3
d[0][2] = 1
d[1][0] = 3
d[1][1] = 2
d[1][2] = 1

# W = np.empty([2, 500])
W = np.full([2, 500], 0.5)
y1 = list(df['saveX'])
y2 = list(df['saveY'])
x1 = list(df['savePitch'])
x2 = list(df['saveRoll'])

def normalize_y1(x):
    result = round(resolution*(x - min(y1))/(max(y1)-min(y1)))
    if result >= resolution:
        return result - 1
    else:
        return result


def normalize_y2(x):
    result = round(resolution*(x - min(y2))/(max(y2)-min(y2)))
    if result >= resolution:
        return result - 1
    else:
        return result


def normalize_x1(x):
    result = round(resolution*(x - min(x1))/(max(x1)-min(x1)))
    if result >= resolution:
        return result - 1
    else:
        return result


def normalize_x2(x):
    result = round(resolution*(x - min(x2))/(max(x2)-min(x2)))
    if result >= resolution:
        return result - 1
    else:
        return result


def cmac_hash(p):
    r_k = round((resolution - 2)/n_a) + 2
    h = 0
    # print("r_k:", r_k, "h:", h)
    for i in range(0, n_y):
        h = h*r_k + p[i]
    return int(h)


def table_index(y):
    # y is two scalar input
    p = np.empty([n_a, n_y])
    miu = np.empty([3])
    for i in range(0, n_a):
        for j in range(0, n_y):
            p[i][j] = math.ceil((y[j] + d[j][i])/n_a)
        miu[i] = cmac_hash(p[i])
    return miu


def cmac_mapping(y):
    # output x_predict
    miu = table_index(y)   # miu1,2,3

    x = np.empty([2])
    for i in range(0, 2):
        x[i] = 0
        for j in range(0, n_a):
            x[i] += W[i][int(miu[j])]
    return x


def cmac_train(y, x_pred, x_true):
    miu = table_index(y)  # miu1,2,3
    for i in range(0, n_x):
        error = x_true - x_pred
        print("error:", error)
        increment = lr*error[i]/n_a
        # print("increment:", increment)
        for j in range(0, n_a):
            W[i][int(miu[j])] += increment


y1_norm = list(map(normalize_y1, y1))
y2_norm = list(map(normalize_y2, y2))
x1_norm = list(map(normalize_x1, x1))
x2_norm = list(map(normalize_x2, x2))
y = [y1_norm, y2_norm]
x = [x1_norm, x2_norm]
"""
y_test = [22, 41]
x_test = [12, 32]
miu = table_index(y_test)
print(miu)

x_test_pred = cmac_mapping(y_test)
print(x_test_pred)

for i in range(0, 1000):
    cmac_train(y_test, x_test_pred, x_test)
    x_test_pred = cmac_mapping(y_test)
    print(x_test_pred)
"""

for epoch in range(0, 1000):
    print("--------------------epoch", epoch, "------------------------")
    for i in range(0, len(y1_norm)):
        y_pair = [y[0][i], y[1][i]]
        x_pair = [x[0][i], x[1][i]]
        x_pred = cmac_mapping(y_pair)
        cmac_train(y_pair, x_pred, x_pair)
        print("pred:", x_pred, "true:", x_pair)