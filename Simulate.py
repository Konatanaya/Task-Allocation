import matplotlib.pyplot as plt
import numpy as np
from Useragent import UserAgent
import Approach

timeStep = 500
budget = 10000
userlist = set()
ratesList = []


def initUserList():
    for index in range(200):
        user = UserAgent(index, 8)
        userlist.add(user)


def resetUserList():
    for user in userlist:
        user.reset()


def drawPlot():
    mark = ['-o','-*','-v','-+','-x','-']
    #mark = ['-', ':', '-.', '_', '-x']
    x = np.linspace(0, timeStep+1, timeStep+1)
    fig = plt.figure()
    plt.subplot(1,2,1)
    for index in range(len(ratesList)):
        y = ratesList[index].engagedRate
        plt.plot(x, y, mark[index],label=ratesList[index].printClassName())
    plt.legend(loc='lower right')
    #plt.axis([0,timeStep,0.0,1.0])
    #plt.ylim(0,1.0)
    plt.xlabel("Time step")
    plt.ylabel("Proportion of participating users")

    plt.subplot(1,2,2)
    for index in range(len(ratesList)):
        y = ratesList[index].loss
        plt.plot(x, y, mark[index], label=ratesList[index].printClassName())
    plt.legend(loc='lower right')
    # plt.axis([0,timeStep,0.0,1.0])
    # plt.ylim(0,1.0)
    plt.xlabel("Time step")
    plt.ylabel("Loss in total")
    plt.suptitle("Overall Budget = 10000")
    plt.show()



initUserList()

resetUserList()
control = Approach.Control(timeStep, budget, userlist)
control.simulate()
ratesList.append(control)

resetUserList()
ta = Approach.TA(timeStep, budget, userlist)
ta.simulate()
ratesList.append(ta)

resetUserList()
eve = Approach.EVE1(timeStep, budget, userlist)
eve.simulate()
ratesList.append(eve)

resetUserList()
ucb = Approach.fKUBE(timeStep, budget, userlist)
ucb.simulate()
ratesList.append(ucb)

resetUserList()
eg = Approach.epsilon_greedy(timeStep, budget, userlist, 0.1)
eg.simulate()
ratesList.append(eg)

resetUserList()
ef = Approach.epsilon_first(timeStep, budget, userlist, 0.1)
ef.simulate()
ratesList.append(ef)

drawPlot()
