#! /usr/bin/python -Qnew
# -*- coding: utf-8 -*-
import random, time, os
 
# Automatic Mondrian (Pieter Cornelis "Piet" Mondriaan, 1872-1944)
# GPL 2 by Jean-Christophe BEUMIER - 2014, 28 september -
#  rough&dirty - known bugs:
# 1. lines never cross, since it processes by dividing rectangular fields
#    -> does it worry anybody? 
# 2. a colour (light gray, red, yellow or blue) can be missing
#    -> if you cannot stand it, delete the file and generate another picture
 
# picture dimensions (px) - any size you like, not too little:
width=600
height=400
thick=8 # line width
gray=chr(216) # default colour: very light gray
dark=chr(32) # frame and dividing lines: very dark gray
 
tab=[gray]*width*height*3 # matrix= nbr of pixels (RVB: 3 bytes per colour)
nbr=20 # max number of division
clr=[[chr(255),chr(30),chr(30)],[chr(255),chr(255),chr(64)],[chr(0),chr(100),chr(255)]] # red RVB / yellow RVB / blue RVB : Mondrian colours
 
header="P6 %s %s 255\n" %(width, height) # PNM file colour/binary data
 
# external frame
 
for j in range(0,width):
  for i in range(0,thick):
    point=width*3*i+j*3
    tab[(point)]=dark
    tab[point+1]=dark
    tab[point+2]=dark
  for i in range(height-thick,height):
    point=width*3*i+j*3
    tab[point]=dark
    tab[point+1]=dark
    tab[point+2]=dark
for j in range(0,height):
  for i in range(0,thick):
    point=width*3*j+i*3
    tab[(point)]=dark
    tab[point+1]=dark
    tab[point+2]=dark
  for i in range(width-thick,width):
    point=width*3*j+i*3
    tab[point]=dark
    tab[point+1]=dark
    tab[point+2]=dark
 
for r in range(nbr):
  # random inner point
  x=thick+random.randrange(width-thick*3)
  y=thick+random.randrange(height-thick*3)
 
  flag1=1
  for i in range(-thick,thick*2):
    if tab[(width*y+x+i)*3]!=gray:
      flag1=0 # vertically too close
  flag0=1
  for j in range(-thick,thick*2):
    if tab[(width*(y+j)+x)*3]!=gray:
      flag0=0 # horizontally too close
 
  hasard=random.randrange(2) # vertical (1) or horizontal (0) line
  if hasard==1 and flag1: # vertical ligne, not too close
    prog=0
    while tab[((y-prog-1)*width+x)*3]==gray:
      for i in range(thick):
        tab[((y-prog-1)*width+x+i)*3]=dark
        tab[((y-prog-1)*width+x+i)*3+1]=dark
        tab[((y-prog-1)*width+x+i)*3+2]=dark
      prog+=1
    prog=0
    while tab[((y+prog)*width+x)*3]==gray:
      for i in range(thick):
        tab[((y+prog)*width+x+i)*3]=dark
        tab[((y+prog)*width+x+i)*3+1]=dark
        tab[((y+prog)*width+x+i)*3+2]=dark
      prog+=1
  if hasard==0 and flag0: # horizontal ligne, not too close
    prog=0
    while tab[(width*y+x-prog-1)*3]==gray:
      for i in range(thick):
        tab[(width*(y+i)+x-prog-1)*3]=dark
        tab[(width*(y+i)+x-prog-1)*3+1]=dark
        tab[(width*(y+i)+x-prog-1)*3+2]=dark
      prog+=1
    prog=0
    while tab[(width*y+x+prog)*3]==gray:
      for i in range(thick):
        tab[(width*(y+i)+x+prog)*3]=dark
        tab[(width*(y+i)+x+prog)*3+1]=dark
        tab[(width*(y+i)+x+prog)*3+2]=dark
      prog+=1
 
for r in range(nbr): # attents 'r' times
  x=random.randrange(width)
  y=random.randrange(height)
  if tab[(width*y+x)*3]==gray: # but works only on gray parts of picture
    prog=0
    while tab[(width*y+x+prog-1)*3]==gray:
      prog-=1
    left=x+prog # determining left abscissa of rectangle
    prog=0
    while tab[(width*y+x+prog+1)*3]==gray:
      prog+=1
    right=x+prog # determining right abscissa of rectangle
    prog=0
    while tab[(width*(y+prog-1)+x)*3]==gray:
      prog-=1
    up=y+prog # determining top ordinate of rectangle
    prog=0
    while tab[(width*(y+prog+1)+x)*3]==gray:
      prog+=1 # determining bottom ordinate of rectangle
    down=y+prog
 
    teinte=clr[random.randrange(3)] # random colour of rectangle
    for i in range(left,right+1): # filling rectangle
      for j in range(up,down+1):
       tab[(i+width*j)*3]=teinte[0]
       tab[(i+width*j)*3+1]=teinte[1]
       tab[(i+width*j)*3+2]=teinte[2]
 
image=header+"".join(tab) # header + joining data from list
temps=time.time() # number of second since (UNIX) world creation: 1970.01.01 0h00:00
name="mondrian"+str(temps)
 
han=open(name+".pnm","w") # saving picture
han.write(image)
han.close()
 
try:
  # only with imagemagick on your system:
  os.system("convert "+name+".pnm "+name+".png")
  os.remove(name+".pnm") 
except: # didn't check: imagemagick is on my system
  print """
imagemagick is not on your system
PNM file P6 colour & raw data: width*height*3 bytes
 
 
"""