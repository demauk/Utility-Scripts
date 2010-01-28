#!/usr/bin/python

import sys
import os

if len(sys.argv) < 2:
   print """
      Usage: snes_guillotine.py snes_rom.smc

      This script removes a header from the snes rom specified."""
   sys.exit(1)

if not os.path.exists(sys.argv[1]) or not sys.argv[1].endswith('.smc'):
   print """
      Usage: snes_guillotine.py snes_rom.smc

      The file "%s" doesn't exist or doesn't have the extension .smc. Exiting ...""" % sys.argv[1]
   sys.exit(1)

size = os.path.getsize(sys.argv[1])
if (size % 1024) == 0:
   print """
      Usage: snes_guillotine.py snes_rom.smc

      The size of file "%s" is exactly divisible by 1024.
      It doesn't have a header to remove. Exiting ...""" % sys.argv[1]
   sys.exit(1)


finput = open(sys.argv[1], 'rb')
fname = sys.argv[1]
if fname.find('{HEADER}') != -1:
   fname.replace('{HEADER}', '')
foutput = open(fname.replace('.smc', ' [!].smc'), 'wb')

finput.seek(512)
foutput.write(finput.read())

finput.close()
foutput.flush()

print """
   Wrote "%s". """ % foutput.name

foutput.close()
