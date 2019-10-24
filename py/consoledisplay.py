#!/usr/bin/env python3

import sys

out = ""
for i in range(100000):
	sys.stdout.write("\b"*len(out) + str(i))
	out = str(i)
sys.stdout.write("\n")
sys.stdout.flush()

