import math
import numpy as np
import random


class Approach:
    rate = 1.0

    def __init__(self, time, budget):
        self.timestep = time
        self.budget = budget
        self.budgetPerTime = budget
        self.status = 0.0
        self.loss = [0.0]
        self.engagedRate = [0.0]
        self.beta = 0.1
        self.cost = 0.0

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
                self.budget -= user.taskReward
                if self.budget <= 0:
                    self.budget = 0
                user.taskReward = 0
                return l
            return l
        else:
            user.engagementDegree += self.beta * (0 - user.engagementDegree)
            if user.taskNum != 0:
                l = 1.0 - user.continuousNum / user.taskNum
                self.budget -= user.taskReward * user.continuousNum / user.taskNum
                self.cost = user.taskReward * user.continuousNum / user.taskNum
                if self.budget <= 0:
                    self.budget = 0
            user.continuousNum = 0
            user.taskNum = 0
            user.taskReward = 0
            return l

    def calReward(self, user):
        user.taskReward = user.taskNum * self.rate * (1.0 - self.status)

    def printClassName(self):
        return self.__class__.__name__


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


class TA(Approach):
    def __init__(self, time, budget, userList):
        Approach.__init__(self, time, budget)
        self.userList = userList

    def allocateTask(self, user):
        user.taskNum = math.floor(user.engagementDegree * 10) + 1

    def simulate(self):
        Loss = 0
        for t in range(1, self.timestep + 1):
            engaged = 0
            for user in self.userList:
                if self.budget > 0 and user.taskNum == 0:
                    self.allocateTask(user)
                    self.calReward(user)
                user.takeAction(self)
                Loss += self.checkAction(user)
                engaged += user.engagementDegree
            self.status = engaged / len(self.userList)
            self.loss.append(Loss)
            self.engagedRate.append(self.status)


class EVE1(Approach):
    def __init__(self, time, budget, userList):
        Approach.__init__(self, time, budget)
        self.userList = userList

    def allocateTask(self, user):
        user.taskNum = 1
        user.taskReward = user.taskNum * self.rate * (1.0 - self.status)

    def simulate(self):
        Loss = 0
        for t in range(1, self.timestep + 1):
            engaged = 0
            for user in self.userList:
                if self.budget > 0 and user.taskNum == 0:
                    self.allocateTask(user)
                    self.calReward(user)
                user.takeAction(self)
                Loss += self.checkAction(user)
                engaged += user.engagementDegree
            self.status = engaged / len(self.userList)
            self.loss.append(Loss)
            self.engagedRate.append(self.status)


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


class epsilon_first(Approach):
    def __init__(self, time, budget, userList, epslion):
        Approach.__init__(self, time, budget)
        self.epslion = epslion
        self.userList = userList
        self.exploreBudget = self.budget * epslion
        self.currentArm = 0

    def allocateTask(self, user):
        user.taskNum = self.generateTaskNum(user) + 1

    def explore(self, user):
        user.taskNum = self.currentArm + 1

    def generateTaskNum(self, user):
        value = []
        for index in range(user.task.arm_num):
            value.append(user.task.values[index] / (user.task.costs[index]+0.01))
        return np.argmax(value)

    def checkArm(self,user):
        if self.currentArm < user.task.arm_num-1:
            self.currentArm += 1
        else:
            self.currentArm = 0

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
            if user.taskNum != 0:
                l = 1.0 - user.continuousNum / user.taskNum
                self.budget -= user.taskReward * user.continuousNum / user.taskNum
                self.cost = user.taskReward * user.continuousNum / user.taskNum
                if self.budget <= 0:
                    self.budget = 0
            user.continuousNum = 0
            user.taskNum = 0
            user.taskReward = 0
            self.checkArm(user)
            return l

    def updateArm(self, user):
        if user.taskNum != 0:
            if user.action != 0:
                user.task.updateExplore(user.taskNum - 1, user.continuousNum, self.cost)
            elif user.action == 0 and user.continuousNum == user.taskNum:
                user.task.updateExplore(user.taskNum - 1, user.continuousNum, self.cost)

    def simulate(self):
        Loss = 0
        for t in range(1, self.timestep + 1):
            engaged = 0
            for user in self.userList:
                if self.exploreBudget > 0:
                    if user.taskNum == 0:
                        self.explore(user)
                        self.calReward(user)
                else:
                    if self.budget > 0 and user.taskNum == 0:
                        self.allocateTask(user)
                        self.calReward(user)
                user.takeAction(self)
                self.updateArm(user)
                Loss += self.checkAction(user)
                engaged += user.engagementDegree
            self.status = engaged / len(self.userList)
            self.loss.append(Loss)
            self.engagedRate.append(self.status)


class UCB(Approach):
    def __init__(self, time, budget, userList, optionNum):
        Approach.__init__(self, time, budget)
        self.userList = userList
        self.armCount = []
        self.armValue = []
        self.totalCount = 0
        self.initBandit(optionNum)

    def initBandit(self, optionNum):
        for i in range(optionNum):
            self.armCount.append(1)
            self.armValue.append(0)

    def allocateTask(self, user):
        self.totalCount += 1
        user.taskNum = self.generateTaskNum()
        user.taskReward = user.taskNum * self.rate
        self.armCount[user.taskNum] += 1

    def generateTaskNum(self):
        valueList = []
        for i in range(len(self.armValue)):
            value = self.armValue[i] + math.sqrt(2 * math.log(self.totalCount) / self.armCount[i])
            valueList.append(value)

        list = []
        for value in valueList:
            v = self.budget / (len(self.userList) * (valueList.index(value) + 1))
            list.append(min(value, v))
        index = np.argmax(list)
        return index + 1

    def checkAction(self, user):
        if user.action != 0:
            self.armValue[user.taskNum - 1] -= self.armValue[user.taskNum - 1] / self.totalCount
            user.continuousNum = 0
            user.taskNum = 0
            user.taskReward = 0
            return
        if user.continuousNum == user.taskNum:
            self.armValue[user.taskNum - 1] += (1 - self.armValue[user.taskNum - 1]) / self.totalCount
            self.armCount[user.taskNum - 1] += 1
            user.continuousNum = 0
            user.taskNum = 0
            self.budget -= user.taskReward
            if self.budget <= 0:
                self.budget = 0
            user.taskReward = 0

    def simulate(self):
        count = 0
        for t in range(1, self.timestep + 1):

            for user in self.userList:
                if self.budget > 0 and user.taskNum == 0:
                    self.allocateTask(user)
                user.takeAction(self)
                self.checkAction(user)
                if user.action == 0:
                    count += 1
            rate = count / len(self.userList)
            rate = t * len(self.userList) - count
            self.rates.append(rate)
