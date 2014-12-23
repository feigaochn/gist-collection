#! /usr/bin/python -Qnew
# -*- coding: utf-8 -*-
import os
import time
import math
import random

t0 = time.time()
print("\n Initialisation")

# radius length (px) for cycles k1, k2, k3
k1 = 100+random.randrange(100)
k2 = 50+random.randrange(50)
k3 = 30+random.randrange(30)

# image dimension
centre = k1+k2+k3+5
cote = centre*2

# multiplicity of secondary and tertiary cycles

r2 = random.randrange(10)+3
r3 = random.randrange(14)+6

# clockwise secondary cycle if s2==-1
s2 = random.randrange(2)*2-1
if s2 == 1:
    ss2 = "p"
else:
    ss2 = "m"

# clockwise tertiary cycle if s3==-1
s3 = random.randrange(2)*2-1  # 1 ou -1
if s3 == 1:
    ss3 = "p"
else:
    ss3 = "m"

nom = "spiro-%d-%d%s%d-%d%s%d" % (k1,
                                  k2,
                                  ss2,
                                  r2,
                                  k3,
                                  ss3,
                                  r3)  # filename with params
# header for an ascii-coded black and white PNM file
entete = "P1 %s %s " % (cote, cote)


matrice = ['0']*cote*cote  # white pixels matrix

t1 = time.time()
print("  ", t1-t0, "\n\n Matrix filling", nom+".pnm")

for i in range(8000):
    angle = i*math.pi/4000
    x = int(
        round(
            centre +
            math.cos(angle) *
            k1 +
            math.cos(
                angle *
                r2) *
            k2 +
            math.cos(
                angle *
                r3) *
            k3))
    y = int(
        round(
            centre +
            math.sin(angle) *
            k1 +
            math.sin(
                angle *
                r2) *
            k2 *
            s2 +
            math.sin(
                angle *
                r3) *
            k3 *
            s3))
    matrice[y*cote+x] = "1"        # black pixel
    matrice[y*cote+x+1] = "1"      # right pixel
    matrice[y*cote+cote+x] = "1"   # bottom pixel (a line down)
    matrice[y*cote+cote+x+1] = "1"  # bottom-right pixel

fichier = entete+"".join(matrice)

han = open(nom+".pnm", "w")
han.write(fichier)
han.close()

t2 = time.time()
print("  ", t2-t1, "\n\n File creation", nom+".trace.pnm")

for i in range(1000):  # dotted for primary and secondary cycles
    angle = i*math.pi/500
    x = int(round(centre+math.cos(angle)*k1+math.cos(angle*r2)*k2))
    y = int(round(centre+math.sin(angle)*k1+math.sin(angle*r2)*k2*s2))
    matrice[y*cote+x] = "1"      # setting black pixel

fichier = entete+"".join(matrice)

han = open(nom+".trace.pnm", "w")
han.write(fichier)
han.close()

t3 = time.time()
print("  ", t3-t2, "\n\n  ", t3-t0, "pour le temps global")

print()

# 'eom' must be changed by into your favorite image-viewer
os.system("open "+nom+".pnm &")

q = input(" Save image (O/N): ")
if q == "N" or q == "n":
    os.system("rm "+nom+".pnm")  # rm delete a file (UNIX)
    os.system("rm "+nom+".trace.pnm")
    print("   Not saved image\n")
else:
    print("   Saved image\n")
