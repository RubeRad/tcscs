#! py -3

# The construction of a letter S as designed by Francesco Torniello in 1517
# (Perhaps Luther used this for his Wittenberg theses?)
# As Donald Knuth has 'paraphras[ed] his words into modern mathematical terminology'
# in his paper 'The Letter S'

import math as m
import turtle as t

def xfm(x,s,d): # or y
   return x*s+d


def lineseg(x1,y1, x2,y2, scale=80, shiftx=-360, shifty=-360):
   t.penup()
   t.goto(xfm(x1,scale,shiftx),xfm(y1,scale,shifty))
   t.pendown()
   t.goto(xfm(x2,scale,shiftx),xfm(y2,scale,shifty))


# For a clockwise arc, just call ccw_arc with the
# start/end points switched
def  cw_arc(cx, cy,  sx, sy,  ex, ey, nsteps=20, scale=80, shiftx=-360, shifty=-360):
    ccw_arc(cx, cy,  ex, ey,  sx, sy, nsteps, scale, shiftx, shifty)

# Draw a counter-clockwise arc around center (cx,cy)
# from starting point (sx,sy) to ending point (ex,ey),
# using nsteps short line segments
def ccw_arc(cx, cy,  sx, sy,  ex, ey, nsteps=20, scale=80, shiftx=-360, shifty=-360):

   # Determine the radius
   dx = sx-cx
   dy = sy-cy
   r = m.sqrt(dx*dx + dy*dy)

   # Determine the polar angle of the starting point
   sa = m.degrees( m.atan2(dy, dx) )

   # and the ending point
   dx = ex-cx
   dy = ey-cy
   ea = m.degrees( m.atan2(dy, dx) )

   # make sure we are proceeding from a smaller to a larger angle
   if ea < sa:
      ea += 360

   # Compute the angular step
   da = (ea - sa)/nsteps

   # get ready to start drawing.
   t.penup()
   x = xfm(sx,scale,shiftx)
   y = xfm(sy,scale,shifty)
   a = sa
   t.goto(x,y)
   t.pendown()

   for step in range(nsteps):
      a = a + da
      x = xfm(cx + m.cos(m.radians(a))*r, scale, shiftx)
      y = xfm(cy + m.sin(m.radians(a))*r, scale, shifty)
      t.goto(x,y)



# draw the bounding 9x9 box first
lineseg(0,0,  9,0)
lineseg(9,0,  9,9)
lineseg(9,9,  0,9)
lineseg(0,9,  0,0)

x1 = 4.5    # Point 1 is (4.5, 9)
y1 = 9
cx = 4.5    # a circular arc is drawn from this point with center at (4.5,5.5)
cy = 5.5
x2 = 6      # ending at point 2 where x2=6
y2 = (5.5 + m.sqrt(10)) # Hence y2
cw_arc(cx, cy, x1, y1, x2, y2)  # this arc is CW


cx = 6.5    # A small arc is drawn with center (6.5, 9)
cy = 9
x3 = 6.5    # from point 3 = (6.5, 8.5)
y3 = 8.5
x  = 7      # to (7,9)
y  = 9
ccw_arc(cx, cy, x3, y3, x, y) # this arc is CCW

x4 = 6      # a straight line is drawn from (6,7)
y4 = 7
x5 = (6+16/17) # point 5 has coordinates...
y5 = (8+13/17)
lineseg(x4,y4, x5,y5)

cx = 4      # now an arc is drawn with center (4,7)
cy = 7
x6 = 4      # from point 6 = (4,9)
y6 = 9
x7 = 3      # down to point 7 where x7=3
y7 = (7-m.sqrt(3)) # and y7<7 (hence...)
ccw_arc(cx, cy, x6, y6, x7, y7)

# a straight line is drawn from point 7 to
x8 = 5      # point 8
y8 = 4
lineseg(x7, y7, x8, y8)

cx = 4.5    # an arc centered at ...
cy = (7+1/8)
# is drawn from point 4 to
x9 = 3.5
y9 = 6
ccw_arc(cx, cy, x4, y4, x9, y9)

# and a straight line continues from there to
x10 = 6
y10 = 4.5
lineseg(x9,y9, x10,y10)

# a half-circle runs from this point to point 11
x11 = 3
y11 = 0.5
cx  = 4.5
cy  = 2.5
cw_arc(cx, cy, x10, y10, x11, y11)

# Another small circular arc is now drawn from point 11
cx = 2.5               # with center at (2.5, y)
cy = (1-m.sqrt(3))/2   # [hence y = ...]
x12 = (1 + 7/8)        # to point 12 where
y12 = (m.sqrt(39)+4-4*m.sqrt(3))/8
ccw_arc(cx,cy, x11,y11, x12,y12)

# circular arcs are drawn from point 8 to point 13
cx  = 4   # with center x coordinate
x13 = 4.5 # and with x13
cy  = (4 - m.sqrt(3)) # hence the center y is...
y13 = (4 - m.sqrt(3) - m.sqrt(3.75)) # and y13 = ...
cw_arc(cx,cy, x8,y8, x13,y13)

# and from point 13 to point 14
cx  = 4.5        # with center x coordinate
y14 = 2          # and with y14
cy  = (6 - m.sqrt(3) - m.sqrt(3.75)) # hence the center...
x14 = (4.5 - m.sqrt(4 - y13*y13))
cw_arc(cx,cy, x13,y13, x14,y14)

# Finally a straight line runs from point 14 to point 12
lineseg(x14,y14, x12,y12)




junk = input("enter to exit")













