import math
import numpy as np
import random
from Approach import Approach
from Useragent import UserAgent

class BTA(Approach):
    def __init__(self, time, budget, userList, gamma):
        Approach.__init__(self, time, budget)
        self.gamma = gamma
        self.userList = userList

    def allocateTask(self, user):
        num = user.defaultDif
        for i in (range(user.defaultDif,self.maxTask+1)):
            r_base = (1-self.status) * (1-user.engagementDegree) * (i + math.log(i))
            est = user.lower / math.pow(self.gamma, i-1)
            if est < r_base:
                num = i
                break
        if num == 0:
            num = 1
        user.taskNum = num

    def calculateReward(self, user):
        if self.budget <= 0:
            user.taskReward = 0
        else:
            if user.taskNum != 0:
                r_base = (1-self.status) * (1-user.engagementDegree) * (user.taskNum + math.log(user.taskNum))
                r = min(user.lower/math.pow(self.gamma, user.taskNum - 1), r_base)
                user.taskReward = min(r, self.budget)
            else:
                user.taskReward = 0

    def checkAction(self, user):
        if user.action == 0:
            user.engagementDegree += self.beta * (1 - user.engagementDegree)

            if user.continuousNum == user.taskNum:
                temp = user.taskReward * math.pow(self.gamma, user.taskNum -1)
                temp1 = min(user.lower, temp)
                user.lower = temp1
                if user.taskNum > user.defaultDif:
                    user.defaultDif = user.taskNum
                user.continuousNum = 0
                user.taskNum = 0
                user.success = 1
                self.budget -= user.taskReward
                if self.budget <= 0:
                    self.budget = 0
                user.taskReward = 0
        else:
            if user.taskNum != 0:
                user.success = 0
            user.engagementDegree += self.beta * (0 - user.engagementDegree)
            user.taskNum = 0
            user.taskReward = 0


    def simulate(self):
        Loss = 0
        for t in range(1, self.timestep + 1):
            engaged = 0
            tasknum = 0
            for user in self.userList:
                if self.budget > 0 and user.taskNum == 0:
                    self.allocateTask(user)
                    self.calculateReward(user)
                tasknum += user.taskNum

                user.takeAction(self)
                if user.action != 0:
                    Loss += (1-self.status)
                self.checkAction(user)
                engaged += user.engagementDegree
            self.averageTaskDistribution.append(tasknum / len(self.userList))
            self.status = engaged / len(self.userList)
            self.loss.append(Loss)
            self.engagedRate.append(self.status)
