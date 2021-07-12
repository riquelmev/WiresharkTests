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


# Opens pickle files and sees if there is loss
listOfTxtFiles = []
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
# loops through all files

filesWithLoss = 0
final = []
allStats = []
percentLoss = []
avgRTTData=[]
medRTTData=[]
p95RTTData=[]
timeData = []
throughput = []
windowwithloss = 0
for file in listOfTxtFiles:
    pac = []
    avgLoss = 0
    RTT = []
    lossCount = []
    print("Loop: " + file)
    with open(file, 'rb') as f:
        load = pickle.load(f)
    print(load[0])
    #print(final[1])
    if len(load[0]) > 0:
        pac.append(load[1])
        if load[1] == True:
            filesWithLoss += 1
        for packet in load[0]:
    #            print (packet, packet[9])
            avgLoss += packet[7]
            if type(packet[3]) is float:
                RTT.append(packet[3])
                lossCount.append(packet[7])
        #print(final[0][20:])
        if len(RTT) > 0:
            windowwithloss += 1
            averageRTT = stat.mean(RTT)
            medianRTT = stat.median(RTT)
            p95 = np.percentile(RTT, 95)
            timeInterval = round(load[0][-1][0] - load[0][0][0], 2)
            if timeInterval > 0:

                pac.append(avgLoss)
                pac.append(avgLoss/load[2])
                pac.append(timeInterval)
                pac.append(averageRTT)
                pac.append(medianRTT)
                pac.append(p95)
                bytesPerSec = load[3] / timeInterval
                megabytesPerSec = bytesPerSec / 1000000
                #bytesPerSec2 = load[4] / timeInterval
                #megabytesPerSec2 = bytesPerSec2 / 1000000
                pac.append(megabytesPerSec)

                percentLoss.append(pac[2])
                timeData.append(pac[3])
                avgRTTData.append(pac[4])
                medRTTData.append(pac[5])
                p95RTTData.append(pac[6])
                throughput.append(pac[7])

                final.append(pac)
                #print(RTT,lossCount)
                if load[1] == True:
                #     data = pd.DataFrame(list(zip(RTT, lossCount)))
                #     overall_pearson_r = data.corr().iloc[0,1]
                #     print(overall_pearson_r)
                        #     pac.append(overall_pearson_r)
                    data = pd.DataFrame(zip(RTT, lossCount))

                    print(data)
                    #s = pd.Series(data[0], data[1])

                    plot = pd.plotting.lag_plot(data, lag=1)
                    #plot.set_xlabel("RTT")
                    #plot.set_ylabel("Loss")

                    plt.show()
                    # pd.plotting.lag_plot(data, lag=5)
                    # plt.show()

                #
                #     r_window_size = 50
                #     # Interpolate missing data.
                #     df_interpolated = data.interpolate()
                #     # Compute rolling window synchrony
                #     rolling_r = df_interpolated[0].rolling(window=r_window_size, center=True).corr(df_interpolated[1])
                #     f, ax = plt.subplots(2, 1, figsize=(14, 6), sharex=True)
                #     data.rolling(window=10, center=True).median().plot(ax=ax[0])
                #     ax[0].set(xlabel='Frame', ylabel='Smiling Evidence')
                #     rolling_r.plot(ax=ax[1])
                #     ax[1].set(xlabel='Frame', ylabel='Pearson r')
                #     plt.suptitle(file[-20:])
                #     plt.show()

        #r, p = stats.pearsonr(data[0],data[1])
        #print(f"Scipy computed Pearson r: {r} and p-value: {p}")
        #print(data[0][0])'

        # f, ax = plt.subplots(figsize=(7, 3))
        # data.rolling(window=30, center=True).median().plot(ax=ax)
        # ax.set(xlabel='Time', ylabel='Pearson r' + file[-20:])
        # ax.set(title=f"Overall Pearson r for = {np.round(overall_pearson_r, 2), file[-20:]} ")
        # plt.show()

print(final)
allStats.append(filesWithLoss)
allStats.append(filesWithLoss / len(listOfTxtFiles))
allStats.append(stat.mean(percentLoss))
allStats.append(stat.mean(timeData))
allStats.append(stat.mean(avgRTTData))
allStats.append(stat.mean(medRTTData))
allStats.append(stat.mean(p95RTTData))
allStats.append(stat.mean(throughput))
print(sum(percentLoss)/windowwithloss)
print(allStats)

print("For the given folders, the statstics are:")
print("files with loss: ", allStats[0])
print("percent loss: ",allStats[1])
print("avg percent loss:",allStats[2])
print("avg time: ",allStats[3])
print("avg Rtt :",allStats[4])
print("median Rtt:",allStats[5])
print("95th percentile Rtt:",allStats[6])
print("avg throughput:",allStats[7])

#print(filesWithLoss / len(listOfTxtFiles))
#wasThereLoss, Losscount, Percentage, time interval, avg rtt, median rtt,  p95 rtt, throughput


# sorted_data = np.sort(percentLoss)
# yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
# plt.plot(sorted_data, yvals)
# plt.title("Percent Loss per file")
# plt.show()
#
# sorted_data = np.sort(timeData)
# yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
# plt.plot(sorted_data, yvals)
# plt.title("Time Length of Files")
# plt.show()
#
# sorted_data = np.sort(avgRTTData)
# yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
# plt.plot(sorted_data, yvals)
# plt.title("Avg RTT")
# plt.show()
#
# sorted_data = np.sort(medRTTData)
# yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
# plt.plot(sorted_data, yvals)
# plt.title("Median RTT")
# plt.show()
#
# sorted_data = np.sort(p95RTTData)
# yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)
# plt.plot(sorted_data, yvals)
# plt.title("95th Percentile RTT")
# plt.show()



####################
# file = '/Users/Vicente/PycharmProjects/Wireshark/pcaps/12mbps-bbr_output.pickle'
# with open(file, 'rb') as f:
#     load = pickle.load(f)
# filesWithLoss = 0
# final = []
# percentLoss = []
# avgRTTData=[]
# medRTTData=[]
# p95RTTData=[]
# timeData = []
# throughput = []
# print(load)
# if load[1] == True:
#     filesWithLoss += 1
# for packet in load[0]:
# #            print (packet, packet[9])
#     avgLoss += packet[7]
#     if type(packet[3]) is float:
#         RTT.append(packet[3])
#     lossCount.append(packet[7])
# #print(final[0][20:])
# averageRTT = stat.mean(RTT)
# print(averageRTT)
# medianRTT = stat.median(RTT)
# print(medianRTT)
# p95 = np.percentile(RTT, 95)
# print(p95)
# timeInterval = round(load[0][-1][0] - load[0][0][0], 2)
#
# pac.append(avgLoss)
# pac.append(avgLoss/load[2])
# pac.append(timeInterval)
# pac.append(averageRTT)
# pac.append(medianRTT)
# pac.append(p95)
# bytesPerSec = load[3] / timeInterval
# megabytesPerSec = bytesPerSec / 1000000
# #bytesPerSec2 = load[4] / timeInterval
# #megabytesPerSec2 = bytesPerSec2 / 1000000
# pac.append(megabytesPerSec)
#
#
# percentLoss.append(pac[2])
# timeData.append(pac[3])
# avgRTTData.append(pac[4])
# medRTTData.append(pac[5])
# p95RTTData.append(pac[6])
#
# final.append(pac)
# #print(RTT,lossCount)
# print(final)
#
# (print(RTT, lossCount))





# overall_pearson_r = data.corr().iloc[0,1]
# print(overall_pearson_r)
