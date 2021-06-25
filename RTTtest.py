import csv
Mainfile = "/Users/Vicente/PycharmProjects/Wireshark/pcaps/10mbps-unrestricted-randomloss_output.txt"
#Sourcefile = "WireSharkTest6.txt"
#Destfile = "WireSharkTest7.txt"

#Opens txt and extracts the data
with open(Mainfile) as dfile:
    data = dfile.read()
tempMain = []
sentances = data.splitlines()
for sentance in sentances:
    sen = sentance.split()
    tempMain.append(sen)

#determines source and destinations. Assumes the last two packet transfers are from different sources.
#if int(tempMain[-1][4]) > int(tempMain[-2][4]):
#    print(tempMain[-1][3])
#    source = tempMain[-1][3]
#    dest = tempMain[-2][3]
#else:
#    print(tempMain[-2][3])
#    source = tempMain[-2][3]
#    dest = tempMain[-1][3]

current = tempMain[0]
for i in range(len(tempMain)):
    if int(tempMain[i][4]) > int(current[4]):
        #print(tempMain[i])
        current = tempMain[i]
#print(current)
source = current[2]
dest = current[3]
port = current[7]

print(source)
print(dest)
print(port)
print(type(port))

#filters the txt data into two different lists based on source and dest.
sourcePackets=[]
destPackets = []
for packet in tempMain:
    #print(packet)
    if packet[2] == source and int(packet[6]) > 0 and packet[7] == port:
        newPacket = [packet[1],packet[4],packet[6], 'F']
        sourcePackets.append(newPacket)
    if packet[2] == dest and int(packet[6]) == 0:
        newPacket = [packet[1],packet[5]]
        destPackets.append(newPacket)
print(len(sourcePackets))

#Writes CSV containing the destination data. Time and Ack
with open('/Users/Vicente/PycharmProjects/Wireshark/pcaps/10mbps-unrestricted-randomloss_output_DEST.csv','w') as myfile:
    wr = csv.writer(myfile, delimiter= ',')
    for packet in destPackets:
        wr.writerow(packet)


#with open('Source.csv', newline='') as f:
#    reader = csv.reader(f)
#    for row in reader:
#        print(row)

Duplicates=[]
setOfElems = set()
for i in range(len(sourcePackets)):
    if sourcePackets[i][1] in setOfElems:
        Duplicates.append(sourcePackets[i][1])
    else:
        setOfElems.add(sourcePackets[i][1])
    sourcePackets[i][3] = 1

#setOfDups = set()
#for dup in Duplicates:
#    setOfDups.add(dup)

#newDuplicates = set()
#for packet in reversed(sourcePackets):
#    if packet[3] == 'L' and not packet[1] in newDuplicates:
#        packet[3] = 'R'



for dupicate in Duplicates:
    count = 1
    for packet in sourcePackets:
        if packet[1] == dupicate:
            packet[3] = count
            count+=1
#print(Duplicates)
#print(sourcePackets)
#Use first and last to do a count.
#writes time, seq, len, and state to source.csv
dupcount = 0
print(Duplicates)
#calculates rtt if possible
finalSourcePackets = []
for spacket in sourcePackets:
    found = False
    if spacket[1] in Duplicates:
        spacket = [spacket[0], spacket[1], spacket[2], spacket[3], 0]
        dupcount+=1
        finalSourcePackets.append(spacket)
    else:
        for dpacket in destPackets:
            if int(spacket[1]) + int(spacket[2]) == int(dpacket[1]):
                rtt = (float(dpacket[0]) - float(spacket[0]))
                spacket = [spacket[0], spacket[1],spacket[2],spacket[3], rtt]
                finalSourcePackets.append(spacket)
                found = True
                break
                #print(spacket[0],dpacket[0])
        if found == False:
            spacket = [spacket[0], spacket[1], spacket[2], spacket[3], 0]
            finalSourcePackets.append(spacket)
#print(finalSourcePackets)
print(dupcount)


for packet in finalSourcePackets:
    if packet[4] > 0 and packet[1] in Duplicates:
        print('error')
#write time, seq, len, state, and rtt to source2.csv
with open('/Users/Vicente/PycharmProjects/Wireshark/pcaps/10mbps-unrestricted-randomloss_output_SOURCE.csv','w') as myfile:
    wr = csv.writer(myfile, delimiter= ',')
    for packet in finalSourcePackets:
        wr.writerow(packet)
#listOfRetransmits = {}
#for dup in setOfDups:
#    for packet in Duplicates:
#        #if packet[3]
#        print(packet)


#listOfRetransmits = []
#for packet in sourcePackets:
#    if packet[1] in setOfDups:
#        listOfRetransmits.append(packet)
#print(listOfRetransmits)



#with open(Sourcefile) as dfile:
#    data = dfile.read()

#tempSource = []
#sentances = data.splitlines()
#for sentance in sentances:
#    sen = sentance.split()
#    tempSource.append(sen)

#with open(Destfile) as dfile:
#    data = dfile.read()

#tempDest = []
#sentances = data.splitlines()
#for sentance in sentances:
#    sen = sentance.split()
#    tempDest.append(sen)



#totalSource = []

#for i in range(len(tempSource)):
#    newList = [i, tempSource[i][0], tempSource[i][1], tempSource[i][3], tempSource[i][4], 0]
#    totalSource.append(newList)
#print(total)

#for i in range(len(totalSource)):
#    if int(totalSource[i][3]) < int(totalSource[i-1][3]):
#        totalSource[i][5] = 1
#    totalSource[0][5] = 0

#for i in range(len(totalSource)):
#    if int(totalSource[i][5]) == 1:
#       print (totalSource[i])

#totalDest = []

#for i in range(len(tempDest)):
#    newList = [i, tempDest[i][0], tempDest[i][1], tempDest[i][3], tempDest[i][4], 0]
#    totalDest.append(newList)
#print(total)

#for i in range(len(totalDest)):
#    if int(totalDest[i][3]) < int(totalDest[i-1][3]):
#        totalDest[i][5] = 1
#    totalDest[0][5] = 0

#for i in range(len(totalDest)):
#    if int(totalSource[i][5]) == 1:
#        print (totalDest[i])
#print(totalDest)


#def labelDuplicates(sourcePackets,i):
#    oneMore = False;

#    for packet in sourcePackets:
#        if sourcePackets[3] == i and


