import random, math
import matplotlib.pyplot as plt
import numpy as np

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

class approach():
    def __init__(self):
        self.loss = 0.0

class EpsilonGreedy(approach):
    def __init__(self, arm_n, epsilon):
        approach.__init__(self)
        self.arm_n = arm_n
        self.epsilon = epsilon
        self.values = [0.0 for _ in range(self.arm_n)]
        self.counts = [0.0 for _ in range(self.arm_n)]

    def update(self, arm, reward):
        self.counts[arm] += 1
        self.values[arm] += (reward - self.values[arm]) / self.counts[arm]
        self.loss += 1 - reward

    def pull(self):
        if random.random() < self.epsilon:
            return random.choice(range(self.arm_n))
        else:
            m = max(self.values)
            return self.values.index(m)
'''
arms = [0.3,0.3,0.8]
rate = []
eg = EpsilonGreedy(3,0.1)
for i in range(timestep):
    selected = eg.pull()
    if random.random()<arms[selected]:
        reward = 1
    else:
        reward = 0
    eg.update(selected,reward)
    rate.append(eg.loss)
ratesList.append(rate)

rate = []
eg = EpsilonGreedy(3,0.01)
for i in range(timestep):
    selected = eg.pull()
    if random.random()<arms[selected]:
        reward = 1
    else:
        reward = 0
    eg.update(selected,reward)
    rate.append(eg.loss)
ratesList.append(rate)

'''
drawPlot()