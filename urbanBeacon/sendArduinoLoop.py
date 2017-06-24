import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)

pipe = [0xE8, 0xE8, 0xF0, 0xF0, 0xE1]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipe)
radio.printDetails()

testCount = 0;

while True:
	testCount = testCount+1;

	message = list("GET THE STRING"+str(testCount));
	while len(message) < 32:
		message.append(0)

	start = time.time()
	radio.write(message)
	print("Sent the message")
	time.sleep(1)
