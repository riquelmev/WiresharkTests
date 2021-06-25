import os
import matplotlib.pyplot as plt
import csv
import pandas as pd
import statistics as stat
from scipy import stats



listOfTxtFiles = []
#Finds the count of all images.
parent_dir = '/Users/Vicente/PycharmProjects/Wireshark/pcaps'
for subdir, dirs, files in os.walk(parent_dir):
    for file in files:
        fi = str.lower(file)
        if fi.endswith('.txt'):
            temp = os.path.join(parent_dir, subdir)
            finalpath = (os.path.join(temp, fi))
            listOfTxtFiles.append(finalpath)

#loops through all files
for file in listOfTxtFiles:
    print("Loop: " + file)
    with open(file) as dfile:
        data = dfile.read()
    tempMain = []
    sentances = data.splitlines()
    for sentance in sentances:
        sen = sentance.split()
        tempMain.append(sen)

    #determines proper source, dest, and port
    current = tempMain[0]
    for i in range(len(tempMain)):
        if int(tempMain[i][4]) > int(current[4]):
            # print(tempMain[i])
            current = tempMain[i]
    source = current[2]
    dest = current[3]
    port = current[7]

    #skims excess data
    sourcePackets = []
    destPackets = []
    Duplicates = []
    setOfElems = set()
    for packet in tempMain:
        if packet[2] == source and int(packet[6]) > 0 and packet[7] == port:
            newPacket = [packet[1], packet[4], packet[6], 'F']
            sourcePackets.append(newPacket)
        if packet[2] == dest and int(packet[6]) == 0:
            newPacket = [packet[1], packet[5]]
            destPackets.append(newPacket)

# creates proper count based on duplicate seqs
    for i in range(len(sourcePackets)):
        if sourcePackets[i][1] in setOfElems:
            Duplicates.append(sourcePackets[i][1])
        else:
            setOfElems.add(sourcePackets[i][1])
        sourcePackets[i][3] = 1
    for dupicate in Duplicates:
        count = 1
        for packet in sourcePackets:
            if packet[1] == dupicate:
                packet[3] = count
                count += 1

    dupcount = 0

    # calculates rtt if possible
    finalSourcePackets = []
    for spacket in sourcePackets:
        found = False
        if spacket[1] in Duplicates:
            spacket = [spacket[0], spacket[1], spacket[2], spacket[3], 0]
            dupcount += 1
            finalSourcePackets.append(spacket)
        else:
            for dpacket in destPackets:
                if int(spacket[1]) + int(spacket[2]) == int(dpacket[1]):
                    rtt = (float(dpacket[0]) - float(spacket[0]))
                    spacket = [spacket[0], spacket[1], spacket[2], spacket[3], rtt]
                    finalSourcePackets.append(spacket)
                    found = True
                    break
                    # print(spacket[0],dpacket[0])
            if found == False:
                spacket = [spacket[0], spacket[1], spacket[2], spacket[3], 0]
                finalSourcePackets.append(spacket)
    print(finalSourcePackets)

    #Plots graph of RTT
    #rows = []
    #x = []
    #y = []
    #for i in range(len(finalSourcePackets)):
    #    if finalSourcePackets[i][4] != '0':
    #        x.append(float(rows[i][0]))
    #        y.append(float(rows[i][4]))
    #print(len(x))
    #print(len(y))
    #plt.plot(x, y)
    #plt.show()
    #for packet in finalSourcePackets:
    #    if packet[4] > 0 and packet[1] in Duplicates:
    #        print('error')
    x=[]
    y=[]
    window = 0.05
    start = 0.00
    increment = 0.01
    divisions = []
    temp = []
    lossDiv = []
    lossCount = 0
    for row in finalSourcePackets:
        if float(row[0]) > window:
            start = start + window
            divisions.append(temp)
            temp = []
            lossDiv.append(lossCount)
            lossCount = 0
        if float(row[3]) > 1:
            lossCount += 1
        if float(row[4]) > 0:
#and float(row[0] > start)
            tup = [row[0], row[4]]
            temp.append(tup)
    divisions.append(temp)
    lossDiv.append(lossCount)

    print(divisions)
    sortedDiv = divisions.sort()
    print(sortedDiv)

    count = 0
    packets = []
    timeDiv = []
    rttDiv = []
    for i in range(len(divisions)):
        count += 0.05
        time = []
        rtt = []
        print("The Stats for section " + str(round(count - 0.05, 2)) + " to " + str(round(count, 2)) + " are:")
        for packet in divisions[i]:
            time.append(float(packet[0]))
            rtt.append(float(packet[1]))
        timeDiv.append(time)
        rttDiv.append(rtt)
        if len(divisions[i]) > 1:
            pac = [round(count, 2), min(rtt), max(rtt), stat.mean(rtt), stat.variance(rtt), lossDiv[i]]
        elif len(divisions[i]) == 1:
            pac = [round(count, 2), min(rtt), max(rtt), stat.mean(rtt), "N/A", lossDiv[i]]
        else:
            pac = [round(count, 2), 'N/A', 'N/A', 'N/A', "N/A", lossDiv[i]]
        packets.append(pac)
    #print(len(rttDiv))
    #print(len(timeDiv))
    for i in range(len(rttDiv)):
        if len(rttDiv[i]) > 0:
            slope, intercept, r, p, se = stats.linregress(timeDiv[i], rttDiv[i])
            packets[i].append(slope)
            packets[i].append(intercept)
        else:
            packets[i].append('N/A')
            packets[i].append('N/A')
    #print(packets)

    temp = file[:-4]
    output = (temp + "_RTT.csv")
    with open(output, 'w') as myfile:
        wr = csv.writer(myfile, delimiter=',')
        header = ['time', 'min', 'max', 'mean', 'variance', 'lossCount', 'slope', 'intercept']
        wr.writerow(header)
        for packet in packets:
            wr.writerow(packet)