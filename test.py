import random, math
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom, norm, beta, expon

ratesList = []
timestep = 10000
def drawPlot():
    #x = np.linspace(0, timestep, timestep)
    x = np.linspace(0,10,10)
    plt.figure()
    '''
    for index in ratesList:
        y = index
        plt.plot(x, y)
        '''
    y = [math.exp(-0.1*(x)) for x in x]
    plt.plot(x,y)
    #plt.legend(loc='lower right')
    #plt.axis([0,timeStep,0.0,1.0])
    #plt.ylim(0,1.0)
    plt.xlabel("Time step")
    plt.ylabel("Proportion of participating users")
    plt.show()


a = 2
b = 1

x = np.linspace(1, 5, 5)
y = np.exp(-0.1*(x-1))
plt.plot(x, y, label="e")
y = np.power(0.9,x-1)
plt.plot(x, y,label="6")
plt.title('Beta: a=%.1f,b=%.1f' % (a, b))
plt.legend(loc='lower right')
plt.xlabel('x')
plt.ylabel('density')
plt.show()
