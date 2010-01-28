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
bytes = f_in.read()
count = 0
padding = bytes[len(bytes) - 1]
pad_hex = padding.encode('hex')

print 'Last byte is 0x%s' % pad_hex

if pad_hex != '00' and pad_hex != 'ff':
	print 'No trimming possible. Exiting ...'
	sys.exit(1)

print 'Trimming begins ...'
print '\nOriginal size:%12s %10d' % (hex(len(bytes)), len(bytes))

for b in reversed(bytes):
	if b == padding:
		count += 1
	else:
		break
new_size = len(bytes) - count

print '      Padding:%12s %10d' % (hex(count), count)
print ''.ljust(37, '-')
print ' Trimmed size:%12s %10d' % (hex(new_size), new_size)

print '\nWriting ' + out_name + ' ...'

f_out = open(out_name, 'wb')
f_out.write(bytes)
f_out.truncate(new_size)

f_in.close()
f_out.flush()
f_out.close()

print 'Done.'
