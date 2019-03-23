import math
import numpy as np
import random
from Approach import Approach

class fKUBE(Approach):
    def __init__(self, time, budget, userList):
        Approach.__init__(self, time, budget)
        self.userList = userList
        self.totalCount = 0
        self.exploreStatus = 1
        self.status = 0
        self.count = -1

    def allocateTask(self, user):
        user.taskNum = self.generateTaskNum(user)
        user.task.updateCount(user.taskNum - 1)

    def calReward(self,user,t):
        new_value = []
        for index in range(user.pricing.arm_num):
            if sum(user.pricing.counts)==0:
                F_n = user.pricing.values[index]
            else:
                F_n = user.pricing.values[index]+math.sqrt(2*math.log(t)/user.pricing.counts[index])
            f = self.budget / (200 * user.pricing.price[index])
            new_value.append(min(f,F_n))
        self.count = np.argmax(new_value)
        user.taskReward = user.pricing.price[self.count]



    def generateTaskNum(self, user):
        value = []
        for index in range(user.task.arm_num):
            v = user.task.values[index] + math.sqrt(math.log(sum(user.task.counts)/user.task.counts[index]))
            if user.task.costs[index] == 0:
                value.append(0)
            else:
                value.append(v / (user.task.costs[index]))

        return np.argmax(value)+1

    def explore(self, user):
        user.taskNum = user.task.currentArm + 1
        user.task.updateCount(user.task.currentArm)
        if user.task.currentArm < user.task.arm_num - 1:
            user.task.currentArm += 1
        else:
            user.task.currentArm = -1

    def checkAction(self, user):
        if user.action == 0:
            user.engagementDegree += self.beta * (1 - user.engagementDegree)
            if user.continuousNum == user.taskNum:
                self.budget -= user.taskReward
                self.accepted +=1
                if self.budget <= 0:
                    self.budget = 0
                user.taskReward = 0
                user.continuousNum = 0
                user.taskNum = 0
        else:
            user.engagementDegree += self.beta * (0 - user.engagementDegree)
            user.taskNum = 0
            user.taskReward = 0

    def updateArm(self, user):
        cost = 0.0
        if user.taskNum != 0:
            if user.action != 0:
                user.task.updateExplore(user.taskNum - 1, user.currentFeed, cost)
                user.pricing.updateExplore(self.count, 0)
                user.currentFeed = 0
                #user.pricing.counts[self.count] += 1
            elif user.action == 0:
                user.currentFeed += 1
                if user.continuousNum == user.taskNum:
                    cost = user.taskReward
                    user.task.updateExplore(user.taskNum - 1, user.currentFeed, cost)
                    user.pricing.updateExplore(self.count, 1)
                    #user.pricing.counts[self.count] += 1
                    user.currentFeed = 0

    def simulate(self):
        Loss = 0
        for t in range(1, self.timestep + 1):
            engaged = 0
            tasknum = 0
            self.user_num = 0
            for user in self.userList:
                if self.budget > 0 and user.taskNum == 0:
                    if user.task.currentArm != -1:
                        self.explore(user)
                    else:
                        self.allocateTask(user)
                    self.calReward(user,t)
                    self.offer+=1
                tasknum += user.taskNum

                user.takeAction(self)
                self.updateArm(user)
                if user.action == 0:
                    self.user_num += 1
                self.checkAction(user)
                engaged += user.engagementDegree
            self.status = engaged / len(self.userList)
            self.updateList(t)
            if self.budget <= 0 and self.end == 0:
                self.end = t
        self.conclude()
