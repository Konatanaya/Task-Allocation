import math
import numpy as np
import random
from Approach import Approach

class epsilon_first(Approach):
    def __init__(self, time, budget, userList, epslion):
        Approach.__init__(self, time, budget)
        self.epslion = epslion
        self.userList = userList
        self.exploreBudget = self.budget * epslion

    def allocateTask(self, user):
        user.taskNum = self.generateTaskNum(user) + 1

    def explore(self, user):
        user.taskNum = user.task.currentArm + 1

    def generateTaskNum(self, user):
        value = []
        for index in range(user.task.arm_num):
            value.append(user.task.values[index] / (user.task.costs[index] + 0.01))
        return np.argmax(value)

    def checkArm(self, user):
        if user.task.currentArm < user.task.arm_num - 1:
            user.task.currentArm += 1
        else:
            user.task.currentArm = 0

    def checkAction(self, user):
        l = 0.0
        self.cost = 0.0
        if user.action == 0:
            user.engagementDegree += self.beta * (1 - user.engagementDegree)
            user.continuousNum += 1
            if user.continuousNum == user.taskNum:
                user.continuousNum = 0
                user.taskNum = 0
                self.cost = user.taskReward
                if self.exploreBudget > 0:
                    self.exploreBudget -= user.taskReward
                    self.checkArm(user)
                else:
                    self.budget -= user.taskReward
                if self.budget <= 0:
                    self.budget = 0
                user.taskReward = 0
                return l
            return l
        else:
            user.engagementDegree += self.beta * (0 - user.engagementDegree)
            self.cost = 0.01
            if user.taskNum != 0:
                l = 1.0 - user.continuousNum / user.taskNum
            user.continuousNum = 0
            user.taskNum = 0
            user.taskReward = 0
            self.checkArm(user)
            return l

    def updateArm(self, user):
        if user.taskNum != 0:
            if user.action != 0:
                user.task.updateExplore(user.taskNum - 1, user.continuousNum * (1-self.status), self.cost)
            elif user.action == 0 and user.continuousNum == user.taskNum:
                user.task.updateExplore(user.taskNum - 1, user.continuousNum* (1-self.status), self.cost)

    def simulate(self):
        Loss = 0

        for t in range(1, self.timestep + 1):
            engaged = 0
            tasknum = 0
            for user in self.userList:
                if self.exploreBudget > 0:
                    if user.taskNum == 0:
                        self.explore(user)
                        self.calReward(user)
                else:
                    if self.budget > 0 and user.taskNum == 0:
                        self.allocateTask(user)
                        self.calReward(user)
                tasknum += user.taskNum
                user.takeAction(self)
                self.updateArm(user)
                Loss += self.checkAction(user)
                engaged += user.engagementDegree
            self.averageTaskDistribution.append(tasknum / len(self.userList))
            self.status = engaged / len(self.userList)
            self.loss.append(Loss)
            self.engagedRate.append(self.status)