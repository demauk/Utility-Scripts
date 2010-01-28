#!/usr/bin/env python

import sys
import os
import binascii

for root, dirs, files in os.walk(sys.argv[1]):
	for name in files:
		f = open(os.path.join(root, name))
		print "%15s %8d %08x" % (name, os.fstat(f.fileno()).st_size,
								binascii.crc32(f.read()) & 0xffffffff)
		f.close()

