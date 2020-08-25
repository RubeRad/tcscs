#! /usr/bin/env python3

import argparse
import math
from bitstring import BitArray
from struct import *

def bits2uint(b):
   by = BitArray(bin=b)
   return by.uint

parser = argparse.ArgumentParser("Convert a floating point number to binary and back")
parser.add_argument('--pi',           action='store_true', help='times pi')
parser.add_argument('-d', '--double', action='store_true', help='double precision')
parser.add_argument('-v',             action='store_true', help='verbose')
parser.add_argument('x',              type=float,          help='number')
args = parser.parse_args()

x = args.x
if args.pi:
   x *= math.pi

if args.double:
   bytes = pack('>d', x)
   expo0 = 1
   mant0 = 12
   ebias = 1023
else:
   bytes = pack('>f', x)
   expo0 = 1
   mant0 = 9
   ebias = 127

bits = BitArray(bytes)
bitstr = ''
for bit in bits:
   bitstr += '1' if bit else '0'

ss = bitstr[0:expo0]
es = bitstr[expo0:mant0]
ms = bitstr[mant0:]
si = bits2uint(ss)
ei = bits2uint(es)
mi = bits2uint(ms)

print (ss, es, ms)

if si: print('Sign: -')
else:  print('Sign: +')

subnormal = (ei==0)
ei -= ebias
print('Expo:', ei+ebias, '-', ebias, '=', ei)

mant = 2 ** ei
if subnormal:
   ei += 1
   mant *= 2
   print(' i: 0 x 2^{} (subnormal)'.format(ei, mant))
   tot = 0
else:
   print(' i: 1 x 2^{} = {}'.format(ei, mant))
   tot=mant

mbits = BitArray(bin=ms)
bi = 0
for bit in mbits:
   bi += 1
   ei -= 1
   mant /= 2
   if bit:
      print('{:2}: 1 x 2^{} = {}'.format(bi, ei, mant))
      tot += mant
   elif args.v:
      print('{:2}: 0 x 2^{}'.format(bi, ei))

if si:
   tot *= -1
print('Total:', tot)



stophere=1





