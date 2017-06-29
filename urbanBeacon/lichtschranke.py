import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import sys
import os
import spidev


f = open("mqttIP.txt",'r')
line1=f.readline()
line1 = line1.split("\n")
mqttIP = line1[0]

GPIO.setmode(GPIO.BCM)

pipe = [0xF1, 0xF1, 0xF1, 0xF1, 0xE1]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setPayloadSize(32)
radio.setChannel(0x77)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipe)
radio.startListening()

while True:
	
	while not radio.available(0):
		time.sleep(1/100)

	receivedMessage = []
	radio.read(receivedMessage, radio.getDynamicPayloadSize())
	print("Received: {}".format(receivedMessage))

	print("Translating our received Message into unicode characters")
	string = ""

	for n in receivedMessage:
		if (n >= 32 and n <= 126):
			string += chr(n)

	print("Our received message: {}".format(string))

	if (string == "laserTrigger"):
		os.system("mosquitto_pub -h " + mqttIP + " -d -t topic/state -m 'laserTrigger'")
		print "ok"
