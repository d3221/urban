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
#### MAIN LOOP
####


try:
	while True:
		print getDegrees()
		time.sleep(2)

except KeyboardInterrupt:
    print('interrupted!')
