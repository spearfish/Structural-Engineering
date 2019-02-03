#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 15:08:30 2019

@author: donaldbockoven
"""

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import division
import math
import matplotlib.pyplot as plt
import section_props as secprop

def coord_trans(x,y, xo, yo, angle):
    '''
    given an angle in degrees
    and coordinate to translate about
    return the transformed values of
    the x and y lists
    '''
    theta = math.radians(angle)
    
    x_t = [(i-xo)*math.cos(theta)+(j-yo)*math.sin(theta) for i,j in zip(x, y)]
    y_t = [-1.0*(i-xo)*math.sin(theta)+(j-yo)*math.cos(theta) for i,j in zip(x, y)]
    
    x_t = [i+xo for i in x_t]
    y_t = [j+yo for j in y_t]
    
    
    return x_t, y_t

# KootK
x1 = [0,60,60,120,120,60,60,0,0]
y1 = [0,0,60,60,120,120,180,180,0]

x2 = [8,52,52,8,8]
y2 = [8,8,172,172,8]

x3 = [60,112,112,60,60]
y3 = [68,68,112,112,68]

shape1 = secprop.Section(x1,y1)
shape2 = secprop.Section(x2,y2, False, 1)
shape3 = secprop.Section(x3,y3, False, 1)

# Bar coordinates and As's
xb = [4,17,30,43,56,56,56,56,56,69,82,95,108,116,116,116,116,103,90,77,64,56,56,56,56,43,30,17,4,4,4,4,4,4,4,4,4,4,4,4,4,4]
yb = [4,4,4,4,4,17,30,43,56,64,64,64,64,77,90,103,116,116,116,116,116,129,142,155,168,176,176,176,176,163,150,137,124,111,98,85,72,59,46,33,20,7]
ab = [0.31]*len(xb)

# Es and Ec -- consistent units -- 
Es = 29000000 #psi
Ec = math.pow(150,1.5)*33*math.sqrt(4500) #psi

n = Es/Ec

# Desired neutral axis rotation
# positive = clockwise
na_angle = 90
na_y = 80
# tranform the sections and the bars so the NA
# lies on the horiztonal about the centroid of major
# solid shape

shape1.transformed_vertices(shape1.cx,shape1.cy,na_angle)
shape2.transformed_vertices(shape1.cx,shape1.cy,na_angle)
shape3.transformed_vertices(shape1.cx,shape1.cy,na_angle)

xb_t, yb_t = coord_trans(xb,yb,shape1.cx,shape1.cy,na_angle)

# translate everything to the +x,+y quadrant
xtrans = -1.0*min(shape1.x)
ytrans = -1.0*min(shape1.y)

shape1.translate_vertices(xtrans,ytrans)
shape2.translate_vertices(xtrans,ytrans)
shape3.translate_vertices(xtrans,ytrans)

#translate the bars
xb_t = [i+xtrans for i in xb_t]
yb_t = [j+ytrans for j in yb_t]

as_yb_t = [[ast,j] for ast,j in zip(ab,yb_t)]

# if na_y = 0 assumes you want the Icr for
# the plastic neutral axis

if na_y == 0:
    # using the bisection method step the NA
    # down until Marea above = Marea below
    
    a=max(shape1.y)
    b=min(shape1.y)
    c=0
    mna=0
    
    max_iter = 10000
    tol = 1e-12
    loop = 0
    
    while loop < max_iter:
        c = (a+b)/2.0
        
        # conrete area above the cut line
        cut1 = secprop.split_shape_above_horizontal_line(shape1, c)
        asolid = []
        dysolid = [] 
        for sol_shape in cut1:
            asolid.append(sol_shape.area)
            dysolid.append(sol_shape.cy - c)
        
        msolid = sum([ac*d for ac,d in zip(asolid,dysolid)])
        
        # void area above the cut line
        avoid = []
        dyvoid = []
        cut2 = secprop.split_shape_above_horizontal_line(shape2, c, False, 1)
        cut3 = secprop.split_shape_above_horizontal_line(shape3, c, False, 1)
        for void1_shape in cut2:
            avoid.append(void1_shape.area)
            dyvoid.append(void1_shape.cy - c)
        for void2_shape in cut3:
            avoid.append(void2_shape.area)
            dyvoid.append(void2_shape.cy - c) 
            
        mvoid = sum([av*d for av,d in zip(avoid,dyvoid)])
        
        mconc = msolid + mvoid
        
        ms_above = sum([(n-1)*i[0]*abs((i[1]-c)) for i in as_yb_t if i[1]>c])
        ms_below = sum([n*i[0]*abs((i[1]-c)) for i in as_yb_t if i[1]<c])
        
        mna = mconc + ms_above - ms_below
        
        if mna == 0 or abs((a-b)/2.0) <= tol:
            na_y = c
            loop_count=loop
            loop = max_iter
        elif mna < 1:
            a = c
        else:
            b = c
            
        loop+=1
else:
    cut1 = secprop.split_shape_above_horizontal_line(shape1, na_y)
    cut2 = secprop.split_shape_above_horizontal_line(shape2, na_y, False, 1)
    cut3 = secprop.split_shape_above_horizontal_line(shape2, na_y, False, 1)
  
Isolid = []
for solid in cut1:
    I = solid.parallel_axis_theorem(solid.cx,na_y)
    Isolid.append(I[0])
    
Ivoid = []
for void in cut2:
    I = void.parallel_axis_theorem(void.cx,na_y)
    Ivoid.append(I[0])

for void2 in cut3:
    I = void2.parallel_axis_theorem(void2.cx,na_y)
    Ivoid.append(I[0])    

Ibars_above = sum([(n-1)*i[0]*math.pow(i[1]-na_y,2) for i in as_yb_t if i[1]>=na_y])
Ibars_below = sum([n*i[0]*math.pow(i[1]-na_y,2) for i in as_yb_t if i[1]<na_y])   

Icracked = sum(Isolid)+sum(Ivoid)+Ibars_above+Ibars_below

# plot the section
plt.plot(shape1.x,shape1.y,'r-')
plt.plot(shape2.x,shape2.y,'b-')
plt.plot(shape3.x,shape3.y,'b-')

plt.plot(xb_t,yb_t,'ko', markersize=1)

plt.axhline(y=na_y, color='g', linestyle='--')

for c1 in cut1:
    plt.plot(c1.x,c1.y,'c+-')

for c2 in cut2:
    plt.plot(c2.x,c2.y,'k-')

for c3 in cut3:
    plt.plot(c3.x,c3.y,'k-')
    
plt.plot(shape1.cx,shape1.cy,'k+', markersize=10)

note = 'I,cr = {0:.3f}'.format(Icracked)
note2 = 'PNA,y = {0:.3f}\nAt {1} deg.'.format(na_y, na_angle)

plt.annotate(note, xy=(shape1.cx, shape1.cy))
plt.annotate(note2, xy=(shape1.cx, na_y))

plt.show()
