import os
import matplotlib.pyplot as plt
import csv
import pandas as pd
import statistics as stat
from scipy import stats
import pickle5 as pickle

# parent_dir = '/Users/Vicente/PycharmProjects/Wireshark/pcaps'
# for subdir, dirs, files in os.walk(parent_dir):
#     for file in files:
#         fi = str.lower(file)
#         if fi.endswith('pcap'):
#             temp = os.path.join(parent_dir, subdir)
#             finalpath = (os.path.join(temp, fi))
#             listOfFiles.append(finalpath)
#             #imf.save(new_path, "JPEG")
#
# for file in listOfFiles:
#     temp = file[:-5]
#     output = (parent_dir + "/output.txt")
#     #print (output)
#     var = ' tshark -r '+ file + ' > ' + output + ' -Tfields -e "_ws.col.No." -e "_ws.col.Time" -e ip.src -e "_ws.col.Destination"  -e tcp.seq -e tcp.ack -e tcp.len -e tcp.port -Y tcp'
#     print(var)
#     os.system(var)

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
    sourcePackets = {}
    destPackets = {}
    Duplicates = []
    setOfElems = set()
    for packet in tempMain:
        if packet[2] == source and int(packet[6]) > 0 and packet[7] == port:
            seq = int(packet[4])
            newPacket = [float(packet[1]), seq, int(packet[6])]
            if seq in sourcePackets:
                sourcePackets[seq] = (newPacket, True)
            else:
                sourcePackets[seq] = (newPacket, False)
        if packet[2] == dest and int(packet[6]) == 0:
            seq = int(packet[5])
            newPacket = [float(packet[1]), seq]
            if seq not in destPackets:
                destPackets[seq] = newPacket

# creates proper count based on duplicate seqs. Dont need this
 #   for i in range(len(sourcePackets)):
 #       if sourcePackets[i][1] in setOfElems:
 #           Duplicates.append(sourcePackets[i][1])
 #       else:
 #           setOfElems.add(sourcePackets[i][1])
 #       sourcePackets[i][3] = 1
 #   for dupicate in Duplicates:
 #       count = 1
 #       for packet in sourcePackets:
 #           if packet[1] == dupicate:
 #               packet[3] = count
 #               count += 1

    dupcount = 0

    # calculates rtt if possible
    finalSourcePackets = []
    for seq in sorted(sourcePackets.keys()):
        spacket = sourcePackets[seq]
        RTTpacket = list(spacket[0])
        #print(spacket)
        if spacket[1] == False:
            ack = seq + int(spacket[0][2])
            if ack in destPackets:
                rtt = (float(destPackets[ack][0]) - float(spacket[0][0]))
                RTTpacket.append(rtt)

                #if rtt > 0.06:
                    #print(seq)
            else:
                RTTpacket.append(0)
            RTTpacket.append(False)
        else:
            RTTpacket.append(0)
            RTTpacket.append(True)
        finalSourcePackets.append(RTTpacket)
    finalSourcePackets = finalSourcePackets[10:]
    #print(finalSourcePackets[:20])
    #Plots graph of RTT
    # rows = []
    # x = []
    # y = []
    # for i in range(len(finalSourcePackets)):
    #    if finalSourcePackets[i][3] != 0:
    #        rows.append((float(finalSourcePackets[i][0]), float(finalSourcePackets[i][3])))
    #        #y.append(float(finalSourcePackets[i][3]))
    # rows = sorted(rows)
    # x = [item[0] for item in rows]
    # y = [item[1] for item in rows]
    # print(len(x))
    # print(len(y))
    # plt.plot(x, y)
    # plt.show()
    #     if spacket[1] in Duplicates:
    #         spacket = [spacket[0], spacket[1], spacket[2], spacket[3], 0]
    #         dupcount += 1
    #         finalSourcePackets.append(spacket)
    #     else:
    #         for dpacket in destPackets:
    #             if int(spacket[1]) + int(spacket[2]) == int(dpacket[1]):
    #                 rtt = (float(dpacket[0]) - float(spacket[0]))
    #                 spacket = [spacket[0], spacket[1], spacket[2], spacket[3], rtt]
    #                 finalSourcePackets.append(spacket)
    #                 found = True
    #                 break
    #                 # print(spacket[0],dpacket[0])
    #         if found == False:
    #             spacket = [spacket[0], spacket[1], spacket[2], spacket[3], 0]
    #             finalSourcePackets.append(spacket)
    # print(finalSourcePackets)

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
#     x=[]
#     y=[]
#     window = 0.05
#     start = 0.00
#     increment = 0.01
    divisions = []
        #
    temp = []
    #     lossDiv = []
    #     lossCount = 0


    #Might need to ignore packets around loss
    finished = False
    window = 0.05
    start = 0.00
    end = start + window
    increment = 0.01
    temp=[]
    finalPac = []
    final = []
    start = finalSourcePackets[0][0]
    end = finalSourcePackets[-1][0]
    lossCount = 0
    wasThereLoss = False
    for packet in finalSourcePackets:
        if start + window > end:
            break
        if packet[0] < start + window:
            temp.append(packet)
        else:
            #print(start, start + window, temp[0][0],temp[-1][0], temp[0][0] - temp[-1][0], len(temp))
            rtt = []
            timeDiv=[]
            lossCount = 0
            for tpacket in temp:
                if tpacket[3] > 0:
                    rtt.append(tpacket[3])
                    timeDiv.append(tpacket[0])
                if tpacket[4] == True:
                    lossCount += 1
            if len(rtt) > 1:
                pac = [round(start, 2), min(rtt), max(rtt), stat.mean(rtt), stat.variance(rtt)]
            elif len(rtt) == 1:
                pac = [round(start, 2), min(rtt), max(rtt), stat.mean(rtt), 'N/A']
            elif len(rtt) == 0:
                pac = [round(start, 2), 'N/A', 'N/A', 'N/A', 'N/A']
            if len(rtt) > 1:
                slope, intercept, r, p, se = stats.linregress(timeDiv, rtt)
                pac.append(slope)
                pac.append(intercept)
            else:
                pac.append('N/A')
                pac.append('N/A')
            pac.append(lossCount)
            if lossCount > 0:
                #print (pac)
                wasThereLoss = True
                #print(packets)
            #print(pac)
            finalPac.append(pac)
            start += increment
            final = []
            for tpacket in temp:
                if tpacket[0] > start:
                    final.append(tpacket)
                    #temp.remove(tpacket)
            temp = final
    finalPac = [finalPac,wasThereLoss]

#for pac in finalPac:
#    print(pac)



# while finished == False:
#     for row in finalSourcePackets:
#         print(row,start,end)
#         if row[3] > 0 and (row[0]) < end and row[0] > start:
#              temp.append(row)
#         if row[0] > end:
#             divisions.append(temp)
#             temp = []
#             start = start + increment
#             end = end + increment
#             print("breaking")
#             break
#         if start + window > finalSourcePackets[-1][0]:
#             finished = True
# print (divisions)
#             start = start + window
#             divisions.append(temp)
#             temp = []
#             lossDiv.append(lossCount)
#             lossCount = 0
#         if float(row[3]) > 1:
#             lossCount += 1
#         if float(row[4]) > 0:
# #and float(row[0] > start)
#             tup = [row[0], row[4]]
#             temp.append(tup)
#     divisions.append(temp)
#     lossDiv.append(lossCount)
#
#     print(divisions)
#     sortedDiv = divisions.sort()
#     print(sortedDiv)
#
#     count = 0
#     packets = []
#     timeDiv = []
#     rttDiv = []
#     for i in range(len(divisions)):
#         count += 0.05
#         time = []
#         rtt = []
#         print("The Stats for section " + str(round(count - 0.05, 2)) + " to " + str(round(count, 2)) + " are:")
#         for packet in divisions[i]:
#             time.append(float(packet[0]))
#             rtt.append(float(packet[1]))
#         timeDiv.append(time)
#         rttDiv.append(rtt)
#         if len(divisions[i]) > 1:
#             pac = [round(count, 2), min(rtt), max(rtt), stat.mean(rtt), stat.variance(rtt), lossDiv[i]]
#         elif len(divisions[i]) == 1:
#             pac = [round(count, 2), min(rtt), max(rtt), stat.mean(rtt), "N/A", lossDiv[i]]
#         else:
#             pac = [round(count, 2), 'N/A', 'N/A', 'N/A', "N/A", lossDiv[i]]
#         packets.append(pac)
#     #print(len(rttDiv))
#     #print(len(timeDiv))
#     for i in range(len(rttDiv)):
#         if len(rttDiv[i]) > 0:
#             slope, intercept, r, p, se = stats.linregress(timeDiv[i], rttDiv[i])
#             packets[i].append(slope)
#             packets[i].append(intercept)
#         else:
#             packets[i].append('N/A')
#             packets[i].append('N/A')
#     #print(packets)
#
    # temp = file[:-4]
    # output = (temp + "_RTT.csv")
    # with open(output, 'w') as myfile:
    #     wr = csv.writer(myfile, delimiter=',')
    #     header = ['time', 'min', 'max', 'mean', 'variance', 'lossCount', 'slope', 'intercept']
    #     wr.writerow(header)
    #     for packet in finalPac:
    #         wr.writerow(packet)

    pickleFile = file[:-4]
    pickleFile = pickleFile + '.pickle'
    print(pickleFile)
    with open(pickleFile, 'wb') as f:
        pickle.dump(finalPac,f)

with open('/Users/Vicente/PycharmProjects/Wireshark/pcaps/10mbps-unrestricted-randomloss_output.txt') as dfile:
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
sourcePackets = {}
destPackets = {}
Duplicates = []
setOfElems = set()
for packet in tempMain:
    if packet[2] == source and int(packet[6]) > 0 and packet[7] == port:
        seq = int(packet[4])
        newPacket = [float(packet[1]), seq, int(packet[6])]
        if seq in sourcePackets:
            sourcePackets[seq] = (newPacket, True)
        else:
            sourcePackets[seq] = (newPacket, False)
    if packet[2] == dest and int(packet[6]) == 0:
        seq = int(packet[5])
        newPacket = [float(packet[1]), seq]
        if seq not in destPackets:
            destPackets[seq] = newPacket
#print(sourcePackets)
finalSourcePackets = []
for seq in sorted(sourcePackets.keys()):
    spacket = sourcePackets[seq]
    RTTpacket = list(spacket[0])
    # print(spacket)
    if spacket[1] == False:
        ack = seq + int(spacket[0][2])
        if ack in destPackets:
            rtt = (float(destPackets[ack][0]) - float(spacket[0][0]))
            RTTpacket.append(rtt)

            # if rtt > 0.06:
            # print(seq)
        else:
            RTTpacket.append(0)
        RTTpacket.append(False)
    else:
        RTTpacket.append(0)
        RTTpacket.append(True)
    finalSourcePackets.append(RTTpacket)
finalSourcePackets = finalSourcePackets[10:]
#print(finalSourcePackets)
for packet in finalSourcePackets:
    if packet[4] == True:
        print(packet)

finished = False
window = 0.05
start = 0.00
end = start + window
increment = 0.01
temp=[]
finalPac = []
final = []
start = finalSourcePackets[0][0]
end = finalSourcePackets[-1][0]
lossCount = 0
wasThereLoss = False
for packet in finalSourcePackets:
    if start + window > end:
        break
    if packet[0] < start + window:
        temp.append(packet)
    else:
        #print(start, start + window, temp[0][0],temp[-1][0], temp[0][0] - temp[-1][0], len(temp))
        rtt = []
        timeDiv=[]
        lossCount = 0
        for tpacket in temp:
            #print(tpacket)
            if tpacket[3] > 0:
                rtt.append(tpacket[3])
                timeDiv.append(tpacket[0])
            if tpacket[4] == True:
                ("found something")
                lossCount += 1
        if len(rtt) > 1:
            pac = [round(start, 2), min(rtt), max(rtt), stat.mean(rtt), stat.variance(rtt)]
        if len(rtt) == 1:
            pac = [round(start, 2), min(rtt), max(rtt), stat.mean(rtt), 'N/A']
        if len(rtt) == 0:
            pac = [round(start, 2), 'N/A', 'N/A', 'N/A', 'N/A']
        if len(rtt) > 1:
            slope, intercept, r, p, se = stats.linregress(timeDiv, rtt)
            pac.append(slope)
            pac.append(intercept)
        if lossCount > 0:
            print (pac)
            wasThereLoss = True
        else:
            pac.append('N/A')
            pac.append('N/A')
        pac.append(lossCount)
            #print(packets)
        #print(pac)
        finalPac.append(pac)
        start += increment
        final = []
        for tpacket in temp:
            if tpacket[0] > start:
                final.append(tpacket)
                #temp.remove(tpacket)
        temp = final
finalPac = [finalPac,wasThereLoss]

print(finalPac)