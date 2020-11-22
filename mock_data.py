""" this file creates random data instances
steps:
1) a random number N is generated
2) N beach objects are generated
3) for each beach object, random stats are generated
4) the scenario is presented
5) an input is given as to which beach is chosen
6) the input is recorded
"""

#imports
import random
import numpy as np
import os
import sys
import pickle

#beach class, holds all of the numeric data
class Beach():
    def __init__(self, beach_direction, wind_speed, wind_direction, swell1_height, swell2_height, swell1_period, swell2_period, swell1_direction, swell2_direction, tide_height, water_temp, driving_distance):
        self.beach_direction = beach_direction
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.swell1_height = swell1_height
        self.swell2_height = swell2_height
        self.swell1_period = swell1_period
        self.swell2_period = swell2_period
        self.swell1_direction = swell1_direction
        self.swell2_direction = swell2_direction
        self.tide_height = tide_height
        self.water_temp = water_temp
        self.driving_distance = driving_distance

    def to_np_arr(self):
        return np.array([self.beach_direction, self.wind_speed, self.wind_direction, self.swell1_height, self.swell2_height, self.swell1_period, self.swell2_period, self.swell1_direction, self.swell2_direction, self.tide_height, self.water_temp, self.driving_distance])


#generate random number (step 1)
def random_N():
    return random.randint(1, 4)

def sensible_dir(d):
    i = random.randint(0,3)
    while (i-d)%2==0 and i!=d:
        i = random.randint(0,3)
    return i
#generate random data, and create a beach object from it
def random_data():
    beach_direction = random.randint(0,3)
    wind_speed = random.randint(0, 20)
    wind_direction = random.randint(0,3)
    swell1_height = random.uniform(0.5, 10.0)
    swell2_height = random.uniform(0.5, 10.0)
    swell1_period = random.randint(3, 16)
    swell2_period = random.randint(3, 16)
    swell1_direction = sensible_dir(beach_direction)
    swell2_direction = sensible_dir(beach_direction)
    tide = random.uniform(-3.0, 5.0)
    water_temp = random.randint(50, 76)
    driving_distance = random.uniform(0.1, 50.1)
    return Beach(beach_direction, wind_speed, wind_direction, swell1_height, swell2_height, swell1_period, swell2_period, swell1_direction, swell2_direction, tide, water_temp, driving_distance)


""" now that a data instance can be displayed,
1) 10000 data instances will be displayed
2) for each instance, an answer to the top 3 beaches will be given (ranked 1, 2, 3)
3) for each beach in the instance, the features will be stored in a numpy array
4) the responses will also be stored in a numpy array
5) The result data will have X = [[[beach1], [beach2], ...], [[beach1], [beach2], ...], ...]
(3D numpy array where X.length == 1, X[0][i] = data instance, X[0][i][j] = beach j in instance i)

and Y = [[1, 0, 3, ...], [0, 2, 1, ...], ...]
(2D numpy array where Y.length == 10000, Y[0][i] = beach rankings for instance i)
"""


#used to display the beach direction and swell direction
dirs = ['N', 'E', 'S', 'W']
# present the scenario
def present_data():
    if os.path.exists('X_data.npy'):
        X = np.load('X_data.npy')
    else:
        X = [] #overarching numpy array for input

    if os.path.exists('Y_data.npy'):
        Y = np.load('Y_data.npy')
    else:
        Y = [] #overarching numpy array for output
    #generate 5000 instances
    # print(X)
    # print()
    # print(Y)
    for i in range(5000-len(X)):
        instance = [] #nump array that holds an instance
        rankings = [] #numpy array that holds rankings of instance
        beaches = []
        for i in range(3):
            b = random_data()
            beaches.append(b)
            instance.append(b.to_np_arr())
            rankings.append(0) #initially all beaches have a rank of 0
        print('Scenario:                                                ', 'instances completeded: {num}/5000'.format(num = len(X)))
        for key in range(len(beaches)):
            print('beach ', key)
            print('beach_dir: ', dirs[beaches[key].beach_direction])
            print('wind speed: ', beaches[key].wind_speed, ', wind_direction: ', dirs[beaches[key].wind_direction])
            print('swell1 height: ', beaches[key].swell1_height, ', swell1 period: ', beaches[key].swell1_period, ', swell1 direction: ', dirs[beaches[key].swell1_direction])
            print('swell2 height: ', beaches[key].swell2_height, ', swell2 period: ', beaches[key].swell2_period, ', swell2 direction: ', dirs[beaches[key].swell2_direction])
            print('tide: ', beaches[key].tide_height)
            print('water temp: ', beaches[key].water_temp)
            print('driving distance: ',beaches[key].driving_distance)
            print('_________________________________________')
        #now rank the beaches
        first_choice = input('Top Beach: ')
        second_choice = input('Second Best: ')
        third_choice = input('Third Best: ')
        #update ranks
        rankings[int(first_choice)] = 20
        rankings[int(second_choice)] = 10
        rankings[int(third_choice)] = 0
        #add new instance
        if isinstance(X, np.ndarray):
            X = np.insert(X, len(X) -1, np.array(instance), axis = 0)
        else:
            X.append(np.array(instance))
        if isinstance(Y, np.ndarray):
            Y = np.insert(Y, len(Y) -1, np.array(rankings), axis = 0)
        else:
            Y.append(np.array(rankings))
        save = input('Save work?: ')
        if save == 'yes':
            if isinstance(X, np.ndarray):
                np.save('X_data', X)
            else:
                np.save('X_data', np.array(X))
            if isinstance(Y, np.ndarray):
                np.save('Y_data', Y)
            else:
                np.save('Y_data', np.array(Y))
            sys.exit()
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('')


present_data()
# x_dat = np.load('X_data.npy')
# y_dat = np.load('Y_data.npy')
#
# print(x_dat.shape, y_dat.shape)
# from sklearn.linear_model import LinearRegression
# reg = LinearRegression().fit(x_dat.transpose(0,2,1).reshape(750,-1), y_dat)
#
# pkl_file = "linear_reg.pkl"
# with open(pkl_file, 'wb') as file:
#     pickle.dump(reg, file)
