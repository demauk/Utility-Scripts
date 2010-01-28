#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

import sys
import os.path

if len(sys.argv) < 2:
	print '\nUsage: trunc.py filename [output]'
	print 'If output name is not supplied, filename-trim will be used.\n'
	sys.exit(1)

in_name = sys.argv[1]
in_parts = sys.argv[1].rpartition('.')
out_name = in_parts[0] + '-trim.' + in_parts[2]
if len(sys.argv) > 2:
	out_name = sys.argv[2]

if not os.path.exists(in_name) or not os.path.isfile(in_name):
	print 'File %s doesn\'t exist or is a directory. Exiting ...' % in_name
	sys.exit(1)

print 'Reading ' + in_name + ' ...'

f_in = open(in_name, 'rb')
f_in.seek(512)
bytes = f_in.read()

print '\nWriting ' + out_name + ' ...'

f_out = open(out_name, 'wb')
f_out.write(bytes)

f_in.close()
f_out.flush()
f_out.close()

print 'Done.'
