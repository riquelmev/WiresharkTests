import matplotlib.pyplot as plt
import csv
import pandas as pd
rows=[]
x=[]
y=[]
with open('/Users/Vicente/PycharmProjects/Wireshark/pcaps/10mbps-unrestricted-randomloss_output_SOURCE.csv', newline='') as myfile:
    wr = csv.reader(myfile,delimiter=',')
    for row in wr:
        rows.append(row)
       # y.append(row[4])
print(rows[0])
for i in range(len(rows)):
    if rows[i][4] != '0':
        x.append(float(rows[i][0]))
        y.append(float(rows[i][4]))
print(len(x))
print(len(y))
plt.plot(x,y)
plt.show()
#time = [0, 1, 2, 3]
#position = [0, 100, 200, 300]

#plt.plot(time, position)
#plt.xlabel('Time (hr)')
#plt.ylabel('Position (km)')
#plt.show()
