import re
# Match only TCP lines, and either [*,ACK, *] or just [ACK], and grab the ACK id
patt = re.compile(r'(TCP .*\[.*ACK.*\].*Ack=(\d+))')
patt2 = re.compile(r'(TCP .*\[.*ACK\].*Seq=(\d+))')
patt3 = re.compile(r'(TCP .*\[.*ACK\].*Len=(\d+))')
infile = "WireSharkTest.txt"
infile2 = "WireSharkTest2.txt"
print("Opening file...")
with open(infile) as dfile:
    data = dfile.read()
    AckMatches = patt.findall(data)
    SeqMatches = patt2.findall(data)
    LenMatches = patt3.findall(data)
   # print(f"Found {len(AckMatches)} matching patterns, first match line {AckMatches[0][0]}, ack number {AckMatches[1][1]}")
NUM=[]
TIME = []
SOURCE = []
sentances = data.splitlines()
for sentance in sentances:
    sen = sentance.split()
    NUM.append(sen[0])
    TIME.append(sen[1])
    SOURCE.append(sen[2])
ACK = []
for ack in AckMatches:
    ACK.append(ack[1])
#print(ACK)
SEQ = []
for seq in SeqMatches:
    SEQ.append(seq[1])
LEN = []
for length in LenMatches:
    LEN.append(length[1])

#for i in range(len(AckMatches)):
#    print (NUM[i],TIME[i], SOURCE[i],SEQ[i], ACK[i],LEN[i])

with open(infile2) as dfile:
    data = dfile.read()
RTT = data.splitlines()
#print (len(sentences))
print (RTT)
final = []
for i in range(len(AckMatches)):
    temp = (NUM[i],TIME[i], SOURCE[i],SEQ[i], ACK[i],LEN[i],RTT[i])
    final.append(temp)
print (final)
print (final[1000])