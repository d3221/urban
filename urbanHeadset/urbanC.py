import time
import sys
import os
import math
import smbus


#####
##### COMPASS FUNCTIONS
#####

bus = smbus.SMBus(1)
address = 0x1e

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def write_byte(adr, value):
    bus.write_byte_data(address, adr, value)

write_byte(0, 0b00000000) # Set to 8 samples @ 15 Hz
write_byte(1, 0b1111111)  # 1.3 gain LSb / Gauss 1090 (default)
write_byte(2, 0b00000000) # Continuous sampling

scale = 0.92
x_offset = 10
y_offset = -87

def getDegrees():
	x_out = (read_word_2c(3) - x_offset) * scale
	y_out = (read_word_2c(7) - y_offset) * scale
	z_out = (read_word_2c(5)) * scale
	bearing  = math.atan2(y_out, x_out) 
	if (bearing < 0):
	    bearing += 2 * math.pi

	degrees = round(math.degrees(bearing))
	return degrees



####
#### Get the target destination in degrees
####


#DEV: ADD THE NRF24L01 DATA FROM THE MODEL AND REPLACE IT
beaconDirection = 90.0



####
#### MAIN LOOP
####

maxAllowedDifference = 50.0

try:
	while True:
		print "LOOP"
		currentDegrees = getDegrees()
		

		if (currentDegrees < beaconDirection):
			personHeading = "left"
			higher = beaconDirection
			lower = currentDegrees
		else:
			personHeading = "right"
			higher = currentDegrees
			lower = beaconDirection

		degreesDifference = higher-lower

		print degreesDifference
		print "Person is head too much: " + personHeading

		if (degreesDifference > 10.0):
			print "WARNING: Getting too far away!"
                        print "ACTION: Adjust the volume balance"
			balanceReduction = 100-(degreesDifference*100)/100
			if (balanceReduction < 0):
				balanceReduction = balanceReduction*-1

			print "Set the " + str(personHeading) + " side to " + str(balanceReduction)
			
			if (personHeading == "left"):
				leftAudio = str(balanceReduction)
				rightAudio = "100";
			else:
				leftAudio = "100";
				rightAudio = str(balanceReduction)

			os.system("amixer sset Master " + leftAudio + "%," + rightAudio + "% -q")
			print "Setted volume; now play the sound"
			os.system("aplay piepen.wav -N")

			

		print "--------------------"
		
		

		#if (currentDegrees >= 0 and currentDegrees < 90):
		#	print "Zwischen norden und osten"

		time.sleep(1) # give the compass some break!!! :D

except KeyboardInterrupt:
    print('interrupted!')
