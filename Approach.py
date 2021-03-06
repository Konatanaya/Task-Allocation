import math
import numpy as np
import random


class Approach:
    rate = 1.0
    maxTask = 5

    def __init__(self, time, budget):
        self.timestep = time
        self.budget = budget
        self.budgetPerTime = budget
        self.status = 0.0
        self.user_num = 0
        self.loss = [0.0]
        self.engagedRate = [0.0]
        self.beta = 0.1
        #self.cost = 0.0

        self.achievementRate = [0.0]
        self.averageTaskDistribution = [0.0]

        self.name = ""

        self.end = 0
        self.offer = 0
        self.accepted = 0

    def setLabelName(self,name):
        self.name= name

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

    def calReward(self, user):
        if self.budget <= 0:
            user.taskReward = 0
        else:
            if user.taskNum != 0:
                r = (1-self.status) * (user.taskNum + math.log(user.taskNum))
                user.taskReward = min(r, self.budget)
            else:
                user.taskReward = 0

    def conclude(self):
        success = self.accepted
        #print(self.name+" "+str(self.offer)+" "+str(self.accepted)+" "+str(success)+" "+str(self.end))

    def printClassName(self):
        return self.__class__.__name__

    def calculateReward(self, user):
        user.taskReward *= user.continuousNum/user.taskNum
        self.budget -= user.taskReward
        if self.budget <= 0:
            self.budget = 0
    def updateList(self,t):
        if t%20 == 0:
            self.loss.append(self.user_num)
            self.engagedRate.append(self.status)

class Control(Approach):
    def __init__(self, time, budget, userList):
        Approach.__init__(self, time, budget)
        self.userList = userList

    def simulate(self):
        Loss = 0
        for t in range(1, self.timestep + 1):
            self.budget += self.budgetPerTime
            engaged = 0
            for user in self.userList:
                user.takeAction(self)
                Loss += self.checkAction(user)
                engaged += user.engagementDegree
            engagedRate = engaged / len(self.userList)
            self.loss.append(Loss)
            self.engagedRate.append(engagedRate)








class epsilon_greedy(Approach):
    def __init__(self, time, budget, userList, epslion):
        Approach.__init__(self, time, budget)
        self.epslion = epslion
        self.userList = userList

    def allocateTask(self, user):
        user.taskNum = self.generateTaskNum(user) + 1

    def generateTaskNum(self, user):
        if max(user.task.values) == 0.0:
            return 0
        if random.random() < self.epslion:
            return random.choice(range(user.task.arm_num))
        else:
            m = max(user.task.values)
            return user.task.values.index(m)

    def updateArm(self, user):
        if user.taskNum != 0:
            if user.action != 0:
                user.task.update(user.taskNum - 1, user.continuousNum)
            elif user.action == 0 and user.continuousNum == user.taskNum:
                user.task.update(user.taskNum - 1, user.continuousNum)

    def simulate(self):
        Loss = 0
        for t in range(1, self.timestep + 1):
            engaged = 0
            for user in self.userList:
                if self.budget > 0 and user.taskNum == 0:
                    self.allocateTask(user)
                    self.calReward(user)
                if self.budget < 0:
                    print(t)
                user.takeAction(self)
                self.updateArm(user)
                Loss += self.checkAction(user)
                engaged += user.engagementDegree
            self.status = engaged / len(self.userList)
            self.loss.append(Loss)
            self.engagedRate.append(self.status)








