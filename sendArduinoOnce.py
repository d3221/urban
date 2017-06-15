import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import sys

GPIO.setmode(GPIO.BCM)

# Build up the radio transmitter
pipe = [0xE8, 0xE8, 0xF0, 0xF0, 0xE1]
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.openWritingPipe(pipe)
#DEV ONLY: radio.printDetails()


###########################
### TRANSMISSION SCRIPT ###
###########################

# Whats the beacon status? [given by sys var from main script]
beaconStatus = str(sys.argv[1])

# Here the message is defnied for the output
message = list("stat:"+beaconStatus);

# If the message has lower than 32 chars, fill it up with 0s
while len(message) < 32:
	message.append(0)

# Publish the message
radio.write(message)

# Give us a note in the console
print("Sent the message")

# Clean the channel up to prevent 'buffering'
GPIO.cleanup()

