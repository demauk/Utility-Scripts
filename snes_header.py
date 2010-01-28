#! /usr/bin/env python

import sys
import os

if len(sys.argv) < 2:
   print """
      Usage: snes_header.py snes_rom.smc

      This script is for the rare case where you want to insert a 512-byte
      header into a snes_rom.smc."""
   sys.exit(1)

if not os.path.exists(sys.argv[1]) or not sys.argv[1].endswith('.smc'):
   print """
      Usage: snes_header.py snes_rom.smc

      The file "%s" doesn't exist or doesn't have the extension .smc. Exiting ...""" % sys.argv[1]
   sys.exit(1)

size = os.path.getsize(sys.argv[1])
if (size % 1024) != 0:
   print """
      Usage: snes_header.py snes_rom.smc

      The size of file "%s" is not evenly divisible by 1024.
      It may already have a header. Exiting ...""" % sys.argv[1]
   sys.exit(1)


finput = open(sys.argv[1], 'rb')
foutput = open(sys.argv[1].replace('.smc', ' {HEADER}.smc'), 'wb')

foutput.write('\x40')
foutput.write(''.join('\x00' for i in range(511)))
foutput.write(finput.read())

finput.close()
foutput.flush()

print """
   Wrote "%s." """ % foutput.name

foutput.close()
