#!/usr/bin/env python

import codecs
import os
import pdb
import re
import subprocess
import sys

VERSION = '0.4'

if not (1 < len(sys.argv) < 4):
  print('This script will try to read a cue file and use it to split a lossless')
  print('audio compilation into individual tracks.')
  print('\nUsage: losslesscuesplit.py <cuefile> [cuefilecodec]')
  print('\nThe cue file codec is optional. Here is a non-exhaustive list of codecs:')
  print('    ascii, big5, euc_jp, gbk, shift_jis, utf_8 (default)')
  print('\nYou might need to install libmac2 and monkeys-audio, as well as:')
  print('    sudo apt-get install flac cuetools shntool\n')
  sys.exit(0)

cuefile = sys.argv[1]
codec = 'UTF_8'
if len(sys.argv) == 3:
  codec = sys.argv[2]
newcuefile, ext = os.path.splitext(cuefile)
newcuefile += ' [UTF_8]' + ext

input = codecs.open(cuefile, 'r', codec)
output = codecs.open(newcuefile, 'w+', 'UTF_8')

reFILE = r'^\s*FILE "(.*)" \w+\s*$'
megafile = ''
status = 'reading the cuefile with {codec} codec'.format(codec=codec)

try:
  for line in input.readlines():
    match = re.search(reFILE, line)
    if match and not megafile:
      megafile = match.group(1)
    output.write(line)

  input.close()
  output.flush()

  # sometimes readline() fails after flush() and seek(0)
  # closing and reopening the file seems to fix it
  # tried to use os.fsync(output.fileno()) instead but it didn't work
  output.close()
  output = codecs.open(newcuefile, 'r', 'UTF_8')

  output.seek(0)
  print('Here are the first ten lines from {file} (whitespace removed)'.format(file=newcuefile))
  for i in range(10):
    print(output.readline().strip())
  output.close()

  goodcodec = raw_input('Does this look right? (y/n) ')[0:1].lower()
  if goodcodec == 'n':
    print('Then the chosen input codec ({cod}) was probably wrong.'.format(cod=codec))
    print('The "[UTF_8]" cue file will be deleted and this script will stop.')
    print('Try a different codec.')
    try:
      os.remove(newcuefile)
    finally:
      sys.exit(0)
  else:
    status = 'piping cuebreakpoints into shnsplit'
    cueproc = subprocess.Popen(['cuebreakpoints', newcuefile],
      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    splitproc = subprocess.Popen(['shnsplit', '-o', 'flac', megafile],
      stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    splitproc.communicate(''.join(cueproc.stdout.readlines()))
    cueproc.wait()
    splitproc.wait()

    status = 'tagging split tracks with cuetag'
    singlefiles = [f for f in os.listdir('.') if re.search(r'^split-track\d\d\.flac$', f)]
    singlefiles.sort()

    tagargs = ['cuetag', newcuefile]
    tagargs.extend(singlefiles)
    tagproc = subprocess.Popen(tagargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = tagproc.communicate()
    if err:
      print(err)
      sys.exit(1)

    status = 'calling cueprint to get track names'
    tracknameproc = subprocess.Popen(['cueprint', '-t', "%t\n", newcuefile],
      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tracknbr = 1
    status = 'renaming tracks'
    for line in tracknameproc.stdout.readlines():
      os.rename('split-track{nbr:02}.flac'.format(nbr=tracknbr),
        '{nbr:02} - {name}.flac'.format(nbr=tracknbr, name=line.strip()))
      tracknbr += 1
except Exception as ex:
  print('There was an error {errortype} while {status}.'.format(
      errortype=type(ex), status=status))
  print(ex)

