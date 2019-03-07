import matplotlib.pyplot as plt
import numpy as np
from Useragent import UserAgent
import Approach, BTA, EpsilonF,fKUBE,EVE,optimal

timeStep = 500
budget = 10000
userlist = set()
ratesList = []


def initUserList(num):
    for index in range(200):
        user = UserAgent(index, num)
        userlist.add(user)


def resetUserList():
    for user in userlist:
        user.reset()


def drawPlot():
    mark = ['-o','-*','-v','-+','-x','-']
    #mark = ['-', ':', '-.', '_', '-x']
    size = 18
    x = np.linspace(0, timeStep+1, timeStep+1)
    fig = plt.figure(figsize=(8,6))
    plt.subplot(1,2,1)

    for index in range(len(ratesList)):
        y = ratesList[index].engagedRate
        plt.plot(x, y, mark[index],label=ratesList[index].name)
    plt.legend(loc='lower right',fontsize=size-4)
    plt.xticks(fontsize=size)
    plt.yticks(fontsize=size)
    #plt.axis([0,timeStep,0.0,1.0])
    #plt.ylim(0,1.0)
    ''''
    plt.subplot(1,3,2)
    for index in range(len(ratesList)):
        y = ratesList[index].loss
        plt.plot(x, y, mark[index], label=ratesList[index].printClassName())
    plt.legend(loc='lower right')
    # plt.axis([0,timeStep,0.0,1.0])
    # plt.ylim(0,1.0)
    plt.xlabel("Time step")
    plt.ylabel("Average Difficulty of Task")
'''
    plt.subplot(1, 2, 2)
    for index in range(len(ratesList)):
        y = ratesList[index].averageTaskDistribution
        plt.plot(x, y, mark[index], label=ratesList[index].printClassName())
    plt.legend(loc='lower right')
    # plt.axis([0,timeStep,0.0,1.0])
    # plt.ylim(0,1.0)

    plt.xlabel("Time steps",fontsize=size)
    plt.ylabel("System Status",fontsize=size)
    plt.suptitle("Overall Budget = "+str(budget),fontsize=size)
    plt.show()



initUserList(8)
''''
resetUserList()
control = Approach.Control(timeStep, budget, userlist
control.simulate()
#ratesList.append(control)

for i in range(5):
    resetUserList()
    ta = BTA.BTA(timeStep, budget, userlist, 0.1+0.2*i)
    k = 0.1+0.2*i
    ta.setLabelName("γ="+str(round(0.1+0.2*i,1)))
    ta.simulate()
    ratesList.append(ta)


for i in range(5):
    #resetUserList()
    userlist.clear()
    initUserList((i+1)*2)
    ta = BTA.BTA(timeStep, budget, userlist, 0.9)
    ta.setLabelName("num="+str((i+1)*2))
    ta.simulate()
    ratesList.append(ta)
    
'''
resetUserList()
ta = BTA.BTA(timeStep, budget, userlist, 0.9)
ta.setLabelName("ATG, γ="+str(0.9))
ta.simulate()
ratesList.append(ta)

resetUserList()
eve = EVE.EVE1(timeStep, budget, userlist)
eve.setLabelName('EVE-1')
eve.simulate()
ratesList.append(eve)

resetUserList()
optimal = optimal.EVE1(timeStep, budget, userlist)
optimal.setLabelName('Optimal')
optimal.simulate()
ratesList.append(optimal)

resetUserList()
ucb = fKUBE.fKUBE(timeStep, budget, userlist)
ucb.setLabelName(ucb.printClassName())
ucb.simulate()
ratesList.append(ucb)
'''
resetUserList()
ef = EpsilonF.epsilon_first(timeStep, budget, userlist, 0.1)
ef.setLabelName("ε-first")
ef.simulate()
ratesList.append(ef)
'''
drawPlot()
