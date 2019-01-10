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

    def allocateTask(self, user):
        user.taskNum = self.generateTaskNum(user)
        user.task.updateCount(user.taskNum - 1)

    def explore(self, user):
        user.taskNum = user.task.currentArm
        user.task.updateCount(user.taskNum - 1)

    def generateTaskNum(self, user):
        value = []
        for index in range(user.task.arm_num):
            value.append(user.task.values[index] / (user.task.costs[index]+0.001))
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
            elif user.action == 0:
                user.currentFeed += 1 - self.status
                if user.continuousNum == user.taskNum:
                    cost = user.taskReward
                    user.task.updateExplore(user.taskNum - 1, user.currentFeed, cost)
                    user.currentFeed = 0.0

    def simulate(self):
        Loss = 0
        for t in range(1, self.timestep + 1):
            engaged = 0
            tasknum = 0
            for user in self.userList:
                if self.exploreStatus == 1:
                    if self.exploreBudget>0 and user.taskNum == 0:
                        self.checkArm(user)
                        self.explore(user)
                        self.calReward(user)
                else:
                    if self.budget > 0 and user.taskNum == 0:
                        self.allocateTask(user)
                        self.calReward(user)
                tasknum += user.taskNum
                user.takeAction(self)
                self.updateArm(user)
                if user.taskNum > 0 and user.action != 0:
                    Loss += (1 - self.status)
                self.checkAction(user)
                engaged += user.engagementDegree
            self.averageTaskDistribution.append(tasknum / len(self.userList))
            self.status = engaged / len(self.userList)
            self.loss.append(Loss)
            self.engagedRate.append(self.status)
