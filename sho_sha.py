#! /usr/bin/py -3

from bitstring import BitArray
from struct import *


def xorstr(b0,b1):
   by0 = BitArray(bin=b0)
   by1 = BitArray(bin=b1)
   x = by0 ^ by1
   return BitArray(x).bin

def andstr(b0,b1):
   by0 = BitArray(bin=b0)
   by1 = BitArray(bin=b1)
   x = by0 & by1
   return BitArray(x).bin

def orstr(b0,b1):
   by0 = BitArray(bin=b0)
   by1 = BitArray(bin=b1)
   x = by0 | by1
   return BitArray(x).bin

def notstr(b):
   by = BitArray(bin=b)
   x = ~by
   return BitArray(x).bin

def leftrot(b, n=1, lbl=''):
   left = b[0:n]
   rest = b[n:len(b)]
   print('Leftrotate', n)
   print(b)
   str = '';
   while len(str)<n: str += ' ';
   print(str+rest+left, lbl)
   return rest + left

def int64(b):
   by = BitArray(bin=b)
   x = by.uint
   return x




# SHA1 starts with the same constants as MD5
h0 = '0x67452301'
h1 = '0xEFCDAB89'
h2 = '0x98BADCFE'
h3 = '0x10325476'
h4 = '0xC3D2E1F0'

msg = 'Cambridge motto: "SDG"'
print('Original Data', len(msg), 'bytes', len(msg)*8, 'bits')
print(msg)
print()
bytes = msg.encode('UTF-8')
barry = BitArray(bytes)
bits  = barry.bin
nbits = len(barry.bin)
bits += '1'
newlen = len(bits)
while len(bits) < 448:
   bits += '0'
len8bytes = pack('>Q', nbits)
bits += BitArray(len8bytes).bin
newlen = len(bits)
#print('512 bits: ')
#print(bits)

words = []
letteri = 0
for i in range(16):
   w = bits[i*32:(i+1)*32]
   if letteri < len(msg):
      li = msg[letteri]
      letteri+=1
   else:
      li = ' '
   if letteri < len(msg):
      lj = msg[letteri]
      letteri+=1
   else:
      lj = ' '
   print('{} {:02d}'.format(w,i))
   words.append(w)

for i in range(16,80):
   print(' ')
   print(words[i-3], i-3)
   print(words[i-8], i-8)
   print(words[i-14], i-14)
   print(words[i-16], i-16)
   w = xorstr(xorstr(words[i-3], words[i-8]),
              xorstr(words[i-14],words[i-16]))
   print('---------------- xor (odd bits)')
   print(w, 'xor')
   w = leftrot(w, 1, str(i))
   words.append(w)


print('')
a = BitArray(h0).bin; print(a, 'a=0x67452301')
b = BitArray(h1).bin; print(b, 'b=0xEFCDAB89')
c = BitArray(h2).bin; print(c, 'c=0x98BADCFE')
d = BitArray(h3).bin; print(d, 'd=0x10325476')
e = BitArray(h4).bin; print(e, 'e=0xC3D2E1F0')

for i in range(80):
   print('\ni =', i, '\n')
   if i<20:
      bc = andstr(b,c)
      print('')
      print(b, 'b')
      print(c, 'c')
      print('-------------------------------- and')
      print(bc, 'b & c')

      bd = andstr(notstr(b), d)
      print('')
      print(notstr(b), 'not b')
      print(d, 'd')
      print('-------------------------------- and')
      print(bd, '~b & d')

      f = orstr(bc,bd)
      print('')
      print(bc, 'b & c')
      print(bd, '~b & d')
      print('-------------------------------- or')
      print(f, 'f = (b & c) | (~b & d)')
      k = BitArray('0x5A827999').bin
      print(k, 'k=sqrt(2)*2^30')
   elif i<40:
      f = xorstr(b, xorstr(c,d))
      k = BitArray('0x6ED9EBA1').bin
      print(k, 'k=sqrt(3)*2^30')
   elif i<60:
      bc = andstr(b, c)
      bd = andstr(b, d)
      cd = andstr(c, d)
      f = orstr(bc, orstr(bd, cd))
      k = BitArray('0x8F1BBCDC').bin
      print(k, 'k=sqrt(5)*2^30')
   else:
      f = xorstr(b, xorstr(c, d))
      k = BitArray('0xCA62C1D6').bin
      print(k, 'k=sqrt(10)*2^30')

   print('')
   al5 = leftrot(a, 5, 'a')
   nal5 = int64(al5)
   nf = int64(f)
   print(f, nf, 'f')
   ne = int64(e)
   print(e, ne, 'e')
   nk = int64(k)
   print(k, nk, 'k')
   nwi = int64(words[i])
   print('{} {} {:02d}'.format(w, nwi, i))
   temp = nal5 + nf + ne + nk + nwi
   print('---------------------------------------------- add')
   btemp = BitArray(hex(temp)).bin
   print(btemp, temp, 'temp')
   print('---------------------------------------------- truncate')
   trunc = 0xFFFFFFFF & temp
   btemp = BitArray(hex(trunc)).bin
   while len(btemp)<32:
      btemp = '0' + btemp
   print(btemp, trunc, 'temp')

   print('abcde before rotation')
   print(a, 'a')
   print(b, 'b')
   print(c, 'c')
   print(d, 'd')
   print(e, 'e')

   e = d
   d = c
   c = leftrot(b,30)
   b = a
   a = btemp

   print('\nAfter rotation')
   print(a, 'a<--temp')
   print(b, 'b<--a')
   print(c, 'c<--(leftrotate b 30)')
   print(d, 'd<--c')
   print(e, 'e<--d')


print('\nFinally, add (and truncate) a-e into h0-h4')
print('h0 ' + h0)
print('a  ' + hex(int64(a)))
print('-------------------------')
h0 = (int(h0,0) + int64(a)) & 0xFFFFFFFF
h0 = hex(h0)
print('h0 ' + h0)
print()

print('h1 ' + h1)
print('b  ' + hex(int64(b)))
print('-------------------------')
h1 = (int(h1,0) + int64(b)) & 0xFFFFFFFF
h1 = hex(h1)
print('h1 ' + h1)
print()

print('h2 ' + h2)
print('c  ' + hex(int64(c)))
print('-------------------------')
h2 = (int(h2,0) + int64(c)) & 0xFFFFFFFF
h2 = hex(h2)
print('h2 ' + h2)
print()

print('h3 ' + h3)
print('d  ' + hex(int64(d)))
print('-------------------------')
h3 = (int(h3,0) + int64(d)) & 0xFFFFFFFF
h3 = hex(h3)
print('h3 ' + h3)
print()

print('h4 ' + h4)
print('e  ' + hex(int64(e)))
print('-------------------------')
h4 = (int(h4,0) + int64(e)) & 0xFFFFFFFF
h4 = hex(h4)
print('h4 ' + h4)
print()

print('Final SHA1 is concatenation of h0-h4:')
sha1 = h0+h1+h2+h3+h4
print(sha1)
