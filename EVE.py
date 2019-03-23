import math
import numpy as np
import random
from Approach import Approach
from Useragent import UserAgent

class EVE1(Approach):
    def __init__(self, time, budget, userList):
        Approach.__init__(self, time, budget)
        self.userList = userList
        self.status = 0

    def allocateTask(self, user):
        user.taskNum = 1

    def checkAction(self, user):
        if user.action == 0:
            user.engagementDegree += self.beta * (1 - user.engagementDegree)

            if user.continuousNum == user.taskNum:
                user.continuousNum = 0
                user.taskNum = 0
                self.accepted+=1
                self.budget -= user.taskReward
                if self.budget <= 0:
                    self.budget = 0
                user.taskReward = 0
        else:
            user.engagementDegree += self.beta * (0 - user.engagementDegree)
            user.taskNum = 0
            user.taskReward = 0

    def calReward(self, user):
        r = (1 - self.status)
        user.taskReward = min( r,user.pre_dif+0.1)

    def simulate(self):
        Loss = 0
        for t in range(1, self.timestep + 1):
            engaged = 0
            tasknum = 0
            self.user_num = 0
            for user in self.userList:
                if self.budget > 0 and user.taskNum == 0:
                    self.allocateTask(user)
                    self.calReward(user)
                    self.offer += 1
                tasknum += user.taskNum

                user.takeAction(self)
                if user.action == 0:
                    self.user_num += 1
                self.checkAction(user)
                engaged += user.engagementDegree
            self.status = engaged / len(self.userList)
            self.updateList(t)
            if self.budget <= 0 and self.end == 0:
                self.end = t
        self.conclude()
