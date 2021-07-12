import os
import matplotlib.pyplot as plt
import csv
import pandas as pd
import statistics as stat
from scipy import stats
import pickle5 as pickle
import numpy as np
import seaborn as sns
import scipy.stats as stats



listOfTxtFiles = []
duplicates = []
# Finds the count of all images.
#parent_dir = '/Users/Vicente/PycharmProjects/Wireshark/pcaps'
parent_dir = '/Users/Vicente/Downloads/2021/06/04'

for subdir, dirs, files in os.walk(parent_dir):
    for file in files:
        fi = str.lower(file)
        if fi.endswith('.pickle'):
            temp = os.path.join(parent_dir, subdir)
            finalpath = (os.path.join(temp, fi))
            listOfTxtFiles.append(finalpath)
#print(listOfTxtFiles)

masterPickle = []
for file in listOfTxtFiles:
    print("Loop: " + file)
    with open(file, 'rb') as f:
        load = pickle.load(f)

    predict5 = []
    trainData20 = []
    if len(load[0]) > 0:
        finalload = list(filter(lambda x: not (any([type(i) == str for i in x])), load[0]))
        #finalload = [[i for i in l if type(i) != str] for l in load[0] if any([type(i) != str for i in l])]
        print(len(load[0]))
        for i in range(int(len(finalload)/20)):
            traindata = finalload[:20]
            finaltrain= []
            for train in traindata:
                train1 = train#[:-2]
                finaltrain.append(train1)

            #print(traindata)
            newload = finalload[20:]
            predict = finalload[:5]
            preholder = []
            windowPac = 0
            for pre in predict:
                windowPac += pre[-1]
                preholder.append(pre[-2])
            #print(preholder)
            #train1 = traindata[:-2]
            if sum(preholder) > 0:
                trainData20.append([finaltrain,sum(preholder)/windowPac])
            else:
                trainData20.append([finaltrain, 0])
    for data in trainData20:
        masterPickle.append(data)

print(len(masterPickle))
print(masterPickle[0])
print(len(masterPickle[0]))
print(masterPickle[0][0])
print(len(masterPickle[0][0]))
print(masterPickle[0][0][0])
print(len(masterPickle[0][0][0]))

loop = 9
for packet in masterPickle:
    if packet[1] > 0:
        for i in range(loop):
            duplicates.append(packet)
    #if packet[1] > 0:
print(len(duplicates))

print(masterPickle[0])
print(duplicates[0])
print(len(masterPickle))
for packet in duplicates:
    masterPickle.append(packet)
#for packet in masterPickle:
#    print(packet[1])

print(len(masterPickle))
pickleFile = 'NNdata'
pickleFile = pickleFile + '.pickle'
print(pickleFile)
with open(pickleFile, 'wb') as f:
    pickle.dump(masterPickle, f)






