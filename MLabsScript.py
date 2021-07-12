import os
#var1 = "tshark -r "/Users/Vicente/Downloads/2021/06/04/ndt-b489l_1621887815_00000000000D5AFC.pcap" > /Users/Vicente/PycharmProjects/Wireshark/WireSharkTest7.txt -Tfields -e "_ws.col.No." -e "_ws.col.Time" -e ip.src -e tcp.seq -e tcp.ack""
#cmd = "ls -%s -%s"%(var1,)
#print(cmd)
#os.system('dir c:\\')


#Prints the count of all images.
#parent_dir = '/Users/Vicente/PycharmProjects/Wireshark/pcaps'
parent_dir = '/Users/Vicente/Downloads/2021/06/04'

count = 0
for subdir, dirs, files in os.walk(parent_dir):
    for file in files:
        im = str.lower(file)
        if im.endswith('.pcap'):
            count+=1
#print(count)

listOfFiles = []
listOfTxtFiles=[]
for subdir, dirs, files in os.walk(parent_dir):
    for file in files:
        fi = str.lower(file)
        if fi.endswith('pcap'):
            temp = os.path.join(parent_dir, subdir)
            finalpath = (os.path.join(temp, fi))
            listOfFiles.append(finalpath)
            #imf.save(new_path, "JPEG")

for file in listOfFiles:
    temp = file[:-5]
    output = (temp + "_output.txt")
    #print (output)
    var = ' tshark -r '+ file + ' > ' + output + ' -Tfields -e "_ws.col.No." -e "_ws.col.Time" -e ip.src -e "_ws.col.Destination"  -e tcp.seq -e tcp.ack -e tcp.len -e tcp.port -Y tcp'
    print(var)
    os.system(var)
