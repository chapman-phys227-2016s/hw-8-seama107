#!\usr\bin\python
"""
File: Particles

Copyright (c) 2016 Michael Seaman

License: MIT

The particles class from cw8, entirely reworked and vectorized in 
numpy arrays to speed up computation time.
"""

import matplotlib
matplotlib.use('Agg')
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
from unittest import TestCase



class Particles():
    def __init__(self, seed = -1):
        self.xPositions = np.zeros(0)
        self.yPositions = np.zeros(0)
        self.step = 0
        self.yLim = [-100, 100]
        self.xLim = [-100, 100]
        if seed == -1:
            self.RNG = np.random.RandomState(np.random.randint(1000000))
        else:
            self.RNG = np.random.RandomState(seed)
        
    def add_particle(self, x = 0, y = 0):
        self.xPositions = np.append(self.xPositions, x)
        self.yPositions = np.append(self.yPositions, y)

    
    def move(self, stepsize = 1):
        random_array = self.RNG.randint(1, 5, len(self.xPositions))
        displacement_arrayX = np.zeros(len(self.xPositions))
        displacement_arrayY = np.zeros(len(self.yPositions))
        displacement_arrayY[random_array == 1] = stepsize #Particles moving north
        displacement_arrayX[random_array == 2] = stepsize #Particles moving east
        displacement_arrayY[random_array == 3] = -1 * stepsize #South
        displacement_arrayX[random_array == 4] = -1 * stepsize #West
        self.xPositions += displacement_arrayX
        self.yPositions += displacement_arrayY

        xBoundaryMask = np.where(abs(self.xPositions) >= 100)
        yBoundaryMask = np.where(abs(self.yPositions) >= 100)
        self.xPositions[xBoundaryMask] -= displacement_arrayX[xBoundaryMask]
        self.yPositions[yBoundaryMask] -= displacement_arrayY[yBoundaryMask]

        dividerMask = np.where(self.xPositions == 0)

        #Now we're dealing with the hole in the divider. We need a vector to store
        #both x and y components at the same time and be able to tell when a particle
        #has the positions 0,-1  0,0  or 0,1 which will be the holes in the divider
        #We'll then take those values and use them as the index to add the displacement array
        #back to them - essentially keeping them where they are

        compositeXY = (self.xPositions * 1000) + self.yPositions
        holeMask = np.where(abs(compositeXY) <= 10)
        self.xPositions[holeMask] += displacement_arrayX[holeMask]
        self.yPositions[holeMask] += displacement_arrayY[holeMask]

        self.xPositions[dividerMask] -= displacement_arrayX[dividerMask]

        self.step += 1
    
    def generate_frame(self):
        fig, ax = plt.subplots(nrows = 1, ncols = 1)
        ax.plot(self.xPositions, self.yPositions, 'k.')
        ax.set_ylim(self.yLim)
        ax.set_xlim(self.xLim)
        fig.savefig('tmp_%05d.png' % (self.step))
        plt.close(fig)
    
    def graph(self):
        plt.plot(self.xPositions, self.yPositions, 'k.')
        plt.axis(self.xLim + self.yLim)
        plt.show()

class Test_Particles(TestCase):
    def test_Particle(self):
        """
        Tests particles created on the same seed to have syncronized movements
        """
        seed_time = int(time.time()*10 % 10000)
        particles1 = Particles(seed_time)
        particles2 = Particles(seed_time)
        for i in xrange(5):
            particles1.add_particle(0,i)
            particles2.add_particle(0,i)
        for i in xrange(5):
            particles1.move()
            particles2.move()
        apt = (particles1.xPositions == particles1.xPositions).all() and (particles1.yPositions == particles1.yPositions).all()
        msg = 'Particles did not move in the same way'
        assert apt, msg
