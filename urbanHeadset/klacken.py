#!/usr/bin/env python
import os
import sys
import time

try:
	while True:
		os.system("aplay -d 10 -q klacken.wav")

except KeyboardInterrupt:
	raise

