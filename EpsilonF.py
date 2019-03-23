import math
import numpy as np
import random
from Approach import Approach


class epsilon_first(Approach):
    def __init__(self, time, budget, userList, epsilon):
        Approach.__init__(self, time, budget)
        self.epsilon = epsilon
        self.userList = userList
        self.exploreBudget = self.budget * self.epsilon
        self.budget -= self.exploreBudget
        self.exploreStatus = 1
        self.count = -1
        self.user_num = 0

    def allocateTask(self, user):
        user.taskNum = self.generateTaskNum(user)
        user.task.updateCount(user.taskNum - 1)

    def explore(self, user):
        user.taskNum = user.task.currentArm + 1
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
        #user.pricing.counts[self.count] += 1

    def generateTaskNum(self, user):
        value = []
        for index in range(user.task.arm_num):
            if user.task.costs[index]==0:
                value.append(0)
            else:
                value.append(user.task.values[index] / (user.task.costs[index]))
        return np.argmax(value)+1

    def checkArm(self, user):
        if user.task.currentArm < user.task.arm_num - 1:
            user.task.currentArm += 1
        else:
            user.task.currentArm = 0

    def checkAction(self, user):
        if user.action == 0:
            user.engagementDegree += self.beta * (1 - user.engagementDegree)
            if user.continuousNum == user.taskNum:
                user.continuousNum = 0
                user.taskNum = 0
                if self.exploreStatus == 1:
                    self.exploreBudget -= user.taskReward
                    if self.exploreBudget <= 0:
                        self.exploreBudget = 0
                        self.exploreStatus = 0
                else:
                    self.budget -= user.taskReward
                    if self.budget <= 0:
                        self.budget = 0
                user.taskReward = 0
        else:
            user.engagementDegree += self.beta * (0 - user.engagementDegree)
            user.taskNum = 0
            user.taskReward = 0

    def updateArm(self, user):
        cost = 0.0
        if user.taskNum != 0:
            if user.action != 0:
                user.task.updateExplore(user.taskNum - 1, user.currentFeed, cost)
                user.currentFeed = 0.0
                user.pricing.updateExplore(self.count, 0)
            elif user.action == 0:
                user.currentFeed += 1
                if user.continuousNum == user.taskNum:
                    self.accepted += 1
                    cost = user.taskReward
                    user.task.updateExplore(user.taskNum - 1, user.currentFeed, cost)
                    user.currentFeed = 0.0
                    user.pricing.updateExplore(self.count, 1)

    def simulate(self):
        Loss = 0
        for t in range(1, self.timestep + 1):
            engaged = 0
            tasknum = 0
            self.user_num = 0
            for user in self.userList:
                if self.exploreStatus == 1:
                    if self.exploreBudget>0 and user.taskNum == 0:
                        self.checkArm(user)
                        self.explore(user)
                        self.calReward(user,t)
                else:
                    if self.budget > 0 and user.taskNum == 0:
                        self.allocateTask(user)
                        self.calReward(user,t)
                tasknum += user.taskNum
                user.takeAction(self)
                self.updateArm(user)
                if user.action == 0:
                    #if t==25:
                     #   print(str(user.taskNum)+" "+str(user.taskReward))
                    self.user_num += 1
                self.checkAction(user)
                engaged += user.engagementDegree
            self.status = engaged / len(self.userList)
            self.updateList(t)
            if self.budget <= 0 and self.end == 0:
                self.end = t