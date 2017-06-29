f = open("mqttIP.txt",'r')
line1=f.readline()
line1 = line1.split("\n")
ip = line1[0]

print ip
