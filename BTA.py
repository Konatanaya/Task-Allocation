import math
import numpy as np
import random
from Approach import Approach

class BTA(Approach):
    def __init__(self, time, budget, userList):
        Approach.__init__(self, time, budget)
        self.userList = userList

    def allocateTask(self, user):
        prior = user.success / (user.success + user.fail)
        user.taskNum = math.floor(self.maxTask * self.status + 1)

    def checkAction(self, user):
        l = 0.0
        self.cost = 0.0
        if user.action == 0:
            user.engagementDegree += self.beta * (1 - user.engagementDegree)
            user.continuousNum += 1
            if user.continuousNum == user.taskNum:
                user.success += 1
                user.continuousNum = 0
                user.taskNum = 0
                self.cost = user.taskReward
                self.budget -= user.taskReward
                if self.budget <= 0:
                    self.budget = 0
                user.taskReward = 0
                return l
            return 1
        else:
            user.engagementDegree += self.beta * (0 - user.engagementDegree)
            user.fail += 1
            if user.taskNum != 0:
                l = 1 - user.continuousNum/user.taskNum
                '''
                self.budget -= user.taskReward * user.continuousNum / user.taskNum
                self.cost = user.taskReward * user.continuousNum / user.taskNum
                if self.budget <= 0:
                    self.budget = 0
                '''
            user.continuousNum = 0
            user.taskNum = 0
            user.taskReward = 0
            return l

    def simulate(self):
        Loss = 0
        for t in range(1, self.timestep + 1):
            engaged = 0
            tasknum = 0
            for user in self.userList:
                if self.budget > 0 and user.taskNum == 0:
                    self.allocateTask(user)
                    self.calReward(user)
                tasknum += user.taskNum
                user.takeAction(self)
                Loss += self.checkAction(user)
                engaged += user.engagementDegree
            self.averageTaskDistribution.append(tasknum / len(self.userList))
            self.status = engaged / len(self.userList)
            self.loss.append(Loss)
            self.engagedRate.append(self.status)