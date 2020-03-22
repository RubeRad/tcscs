#! py -3

# The construction of a letter S as designed by Francesco Torniello in 1517
# (Perhaps Luther used this for his Wittenberg theses?)
# As Donald Knuth has 'paraphras[ed] his words into modern mathematical terminology'
# in his paper 'The Letter S'

import math as m
import turtle as t

def lineseg(x1,y1, x2,y2):
   t.penup()
   t.goto(x1,y1)
   t.pendown()
   t.goto(x2,y2)


def ccw_arc(cx, cy, sx, sy, ex, ey, reflex=False):
   # go to the starting point
   t.penup()
   t.goto(sx, sy)  # this is where we start

   # we need to be oriented so that the center is straight left
   # first point straight at the center
   ctr_heading = t.towards(cx,cy)
   t.setheading(ctr_heading)
   t.right(90)

   # compute the radius
   sdx = sx-cx
   sdy = sy-cy
   r = m.sqrt(sdx*sdx + sdy*sdy)
   sdx /= r # unitize the vector
   sdy /= r

   # determine the number of degrees of arc
   edx = (ex-cx)/r
   edy = (ey-cy)/r
   dot = (sdx*edx + sdy*edy)
   arc = m.degrees(m.acos(dot))
   if reflex:
      arc = 360 - arc

   # now we can finally draw the arc
   t.pendown()
   t.circle(r, arc)


def cw_arc(cx, cy, sx, sy, ex, ey, reflex=False):
   ccw_arc(cx, cy, ex, ey, sx, sy, reflex)


scale = 30

# draw the bounding 9x9 box first
s9 = scale * 9
lineseg(0,0,  s9,0)
lineseg(s9,0, s9,s9)
lineseg(s9,s9, 0,s9)
lineseg(0,s9,  0,0)

x1 = scale * 4.5    # Point 1 is (4.5, 9)
y1 = scale * 9
cx = scale * 4.5    # a circular arc is drawn from this point with center at (4.5,5.5)
cy = scale * 5.5
x2 = scale * 6      # ending at point 2 where x2=6
y2 = scale * (5.5 + m.sqrt(10)) # Hence y2
cw_arc(cx, cy, x1, y1, x2, y2) # this arc is CW


cx = scale * 6.5    # A small arc is drawn with center (6.5, 9)
cy = scale * 9
x3 = scale * 6.5    # from point 3 = (6.5, 8.5)
y3 = scale * 8.5
x  = scale * 7      # to (7,9)
y  = scale * 9
ccw_arc(cx, cy, x3, y3, x, y)  # this arc is CCW

x4 = scale * 6      # a straight line is drawn from (6,7)
y4 = scale * 7
x5 = scale * (6+16/17) # point 5 has coordinates...
y5 = scale * (8+13/17)
lineseg(x4,y4, x5,y5)

cx = scale * 4      # now an arc is drawn with center (4,7)
cy = scale * 7
x6 = scale * 4      # from point 6 = (4,9)
y6 = scale * 9
x7 = scale * 3      # down to point 7 where x7=3
y7 = scale * (7-m.sqrt(3)) # and y7<7 (hence...)
ccw_arc(cx, cy, x6, y6, x7, y7)

# a straight line is drawn from point 7 to
x8 = scale * 5      # point 8
y8 = scale * 4
lineseg(x7, y7, x8, y8)

cx = scale * 4.5    # an arc centered at ...
cy = scale * (7+1/8)
# is drawn from point 4 to
x9 = scale * 3.5
y9 = scale * 6
ccw_arc(cx, cy, x4, y4, x9, y9, True) # this arc is >180

# and a straight line continues from there to
x10 = scale * 6
y10 = scale * 4.5
lineseg(x9,y9, x10,y10)

# a half-circle runs from this point to point 11
x11 = scale * 3
y11 = scale * 0.5
cx  = scale * 4.5
cy  = scale * 2.5
cw_arc(cx, cy, x10, y10, x11, y11)

# Another small circular arc is now drawn from point 11
cx = scale * 2.5               # with center at (2.5, y)
cy = scale * (1-m.sqrt(3))/2   # [hence y = ...]
x12 = scale * (1 + 7/8)        # to point 12 where
y12 = scale * (m.sqrt(39)+4-4*m.sqrt(3))/8
ccw_arc(cx,cy, x11,y11, x12,y12)

# circular arcs are drawn from point 8 to point 13
cx  = scale * 4   # with center x coordinate
x13 = scale * 4.5 # and with x13
cy  = scale * (4 - m.sqrt(3)) # hence the center y is...
y13 = scale * (4 - m.sqrt(3) - m.sqrt(3.75)) # and y13 = ...
cw_arc(cx,cy, x8,y8, x13,y13)

# and from point 13 to point 14
cx  = scale * 4.5        # with center x coordinate
y14 = scale * 2          # and with y14
cy  = scale * (6 - m.sqrt(3) - m.sqrt(3.75)) # hence the center...
x14 = scale * (4.5 - m.sqrt(4 - y13*y13/scale/scale))
cw_arc(cx,cy, x13,y13, x14,y14)

# Finally a straight line runs from point 14 to point 12
lineseg(x14,y14, x12,y12)




junk = input("enter to exit")













