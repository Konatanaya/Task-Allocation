import math
import numpy as np
import random
from Approach import Approach
from Useragent import UserAgent

class EVE1(Approach):
    def __init__(self, time, budget, userList):
        Approach.__init__(self, time, budget)
        self.userList = userList

    def allocateTask(self, user):
        num = 1
        for index in range(2, self.maxTask + 1):
            if user.gamma < math.pow(1 / index, 1 / (index - 1)):
                break
            else:
                num = index
        r_upper = (1 - self.status) * (num + math.log(num))
        r_lower = user.pre_dif / math.pow(user.gamma, num - 1)
        r = min(r_upper, r_lower)
        user.taskNum = num
        user.taskReward = r

    def checkAction(self, user):
        if user.action == 0:
            user.engagementDegree += self.beta * (1 - user.engagementDegree)

            if user.continuousNum == user.taskNum:
                user.continuousNum = 0
                user.taskNum = 0
                self.budget -= user.taskReward
                if self.budget <= 0:
                    self.budget = 0
                user.taskReward = 0
        else:
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
