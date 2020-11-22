import random
import numpy as np
import os
import sys
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def compare(a1, a2):
    max1, max2 = np.amax(a1), np.amax(a2)
    mid1, mid2 = -100, -100
    min1, min2 = -1000, -1000

    for i in range(len(a1)):
        if a1[i] < max1 and a1[i] > mid1:
            mid1 = a1[i]
        if a2[i] < max2 and a2[i] > mid2:
            mid2 = a2[i]

    for i in range(len(a1)):
        if a1[i] < mid1:
            min1 = a1[i]
        if a2[i] < mid2:
            min2 = a2[i]

    r1, r2 = [-1, -1, -1], [-1, -1, -1]

    for i in range(len(a1)):
        if a1[i] == max1:
            r1[0] = i
        if a2[i] == max2:
            r2[0] = i
        if a1[i] == mid1:
            r1[1] = i
        if a2[i] == mid2:
            r2[1] = i
        if a1[i] == min1:
            r1[2] = i
        if a2[i] == min2:
            r2[2] = i

    if r1[0] == r2[0] and r1[1] == r2[1] and r1[2] == r2[2]:
        return True
    else:
        return False


def test_accuracy():
    x = np.load('X_data.npy')
    rmv_noise = []
    for a in x:
        rmv_noise.append(np.delete(np.delete(a, 10, 1), 9, 1))
    rm = np.array(rmv_noise)

    X = rm.transpose(0,2,1).reshape(len(x), -1)
    y_init = np.load('Y_data.npy')

    y_2 = np.where(y_init == 10, 50, y_init)

    y = np.where(y_2==20, 100, y_2)

    #rmv len-2 and len-3






    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    reg = LinearRegression().fit(X_train, y_train)

    pkl_file = "linear_reg2.pkl"
    with open(pkl_file, 'wb') as file:
        pickle.dump(reg, file)

    predict = reg.predict(X_test)

    good = 0
    for i in range(len(predict)):
        if compare(predict[i], y_test[i]):
            good +=1

    print(good/len(predict))

test_accuracy()
