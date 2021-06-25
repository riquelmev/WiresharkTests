import matplotlib.pyplot as plt
import csv
import pandas as pd
import statistics as stat
from scipy import stats
rows=[]
x=[]
y=[]
with open('/Users/Vicente/PycharmProjects/Wireshark/pcaps/12mbps-bbr_SOURCE.csv', newline='') as myfile:
    wr = csv.reader(myfile,delimiter=',')
    for row in wr:
        rows.append(row)
       # y.append(row[4])

window = 0.05
current = 0.05
divisions = []
temp = []
lossDiv = []
lossCount = 0
for row in rows:
    if float(row[0]) > current:
        current = current + window
        divisions.append(temp)
        temp = []
        lossDiv.append(lossCount)
        lossCount = 0
    if float(row[3]) > 1:
        lossCount+=1
        print(row)
    if float(row[4]) > 0:
        tup = [row[0],row[4]]
        temp.append(tup)
divisions.append(temp)
lossDiv.append(lossCount)
count = 0
packets=[]
timeDiv = []
rttDiv = []
for i in range(len(divisions)):
    count += 0.05
    time=[]
    rtt=[]
    print("The Stats for section " + str(round(count - 0.05,2)) + " to " + str(round(count,2)) +  " are:")
    for packet in divisions[i]:
        time.append(float(packet[0]))
        rtt.append(float(packet[1]))
    timeDiv.append(time)
    rttDiv.append(rtt)
    if len(divisions[i]) > 1:
        pac = [round(count,2), min(rtt), max(rtt), stat.mean(rtt), stat.variance(rtt), lossDiv[i]]
        print(pac)
    if len(divisions[i]) == 1:
        pac = [round(count,2), min(rtt), max(rtt), stat.mean(rtt), "N/A", lossDiv[i]]
    else:
        pac = [round(count,2), 'N/A', 'N/A', 'N/A', "N/A", lossDiv[i]]
        print(pac)
    packets.append(pac)
print(len(rttDiv))
print(len(timeDiv))
for i in range(len(rttDiv)):
    if len(rttDiv[i]) > 0:
        slope, intercept, r, p, se = stats.linregress(timeDiv[i],rttDiv[i])
        packets[i].append(slope)
        packets[i].append(intercept)
    else:
        packets[i].append('N/A')
        packets[i].append('N/A')
print(packets)
#print(lossDiv)
#slope, intercept, r, p, se = linregress(x, y)

with open('/Users/Vicente/PycharmProjects/Wireshark/pcaps/12mbps-bbr_RTTStats.csv','w') as myfile:
    wr = csv.writer(myfile, delimiter= ',')
    for packet in packets:
        wr.writerow(packet)

