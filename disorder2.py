#! /usr/bin/env python

"""
File: disorder2.py
Copyright (c) 2016 Michael Seaman
License: MIT

Description: Draws upon the vectorized Particles class to create an animated gif
via commandline
1st argument is the number of steps

"""
from Particles import Particles
import sys
import subprocess

p = Particles()
for i in xrange(1, 99):
    for j in xrange(-99,99):
        p.add_particle(i, j)

p.generate_frame()
for i in range(int(sys.argv[1])):
    for j in range(20):
        p.move()
    p.generate_frame()

subprocess.call("convert -delay 1 -loop 0 *.png GasSimulation.gif", shell=True)
subprocess.call("rm *.png", shell=True)
