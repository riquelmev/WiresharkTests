import os
import matplotlib.pyplot as plt
import csv
import pandas as pd
import statistics as stat
from scipy import stats
import pickle5 as pickle



# Opens pickle files and sees if there is loss
listOfTxtFiles = []
# Finds the count of all images.
parent_dir = '/Users/Vicente/PycharmProjects/Wireshark/pcaps'
for subdir, dirs, files in os.walk(parent_dir):
    for file in files:
        fi = str.lower(file)
        if fi.endswith('.pickle'):
            temp = os.path.join(parent_dir, subdir)
            finalpath = (os.path.join(temp, fi))
            listOfTxtFiles.append(finalpath)
print(listOfTxtFiles)
# loops through all files

filesWithLoss = 0
for file in listOfTxtFiles:
    avgLoss = 0
    print("Loop: " + file)
    with open(file, 'rb') as f:
        final = pickle.load(f)
    print(final[1])
    if final[1] == True:
        filesWithLoss += 1
        for packet in final[0]:
            avgLoss += packet[7]

    print(avgLoss/5)
print(filesWithLoss / len(listOfTxtFiles))

with open('/Users/Vicente/PycharmProjects/Wireshark/pcaps/10mbps-unrestricted-randomloss_output.pickle', 'rb') as f:
    final = pickle.load(f)
for row in final[0]:
    print(row[7])