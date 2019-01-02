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
        user.taskReward = user.taskNum *self.rate* (1-self.status)

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


    def allocateTask(self, user):
        user.taskNum = self.generateTaskNum(user) + 1

    def explore(self, user):
        user.taskNum = user.task.currentArm + 1

    def generateTaskNum(self, user):
        value = []
        for index in range(user.task.arm_num):
            value.append(user.task.values[index] / (user.task.costs[index]+0.01))
        return np.argmax(value)

    def checkArm(self,user):
        if user.task.currentArm < user.task.arm_num-1:
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
            if user.taskNum != 0:
                l = 1.0 - user.continuousNum / user.taskNum
                '''
                if self.exploreBudget > 0:
                    self.exploreBudget -= user.taskReward * user.continuousNum / user.taskNum
                    self.checkArm(user)
                else:
                    self.budget -= user.taskReward * user.continuousNum / user.taskNum
                self.cost = user.taskReward * user.continuousNum / user.taskNum
                if self.budget <= 0:
                    self.budget = 0
                    '''
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


class fKUBE(Approach):
    def __init__(self, time, budget, userList):
        Approach.__init__(self, time, budget)
        self.userList = userList
        self.totalCount = 0

    def allocateTask(self, user):
        user.taskNum = self.generateTaskNum(user)

    def generateTaskNum(self, user):
        value = []
        for index in range(user.task.arm_num):
            value.append((user.task.values[index] + math.sqrt(math.log(sum(user.task.counts))/user.task.counts[index]))/user.task.costs[index])
        return np.argmax(value)

    def explore(self, user):
        user.taskNum = user.task.currentArm + 1

    def checkArm(self,user):
        if user.task.currentArm < user.task.arm_num-1:
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
                self.checkArm(user)
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
                '''
                self.budget -= user.taskReward * user.continuousNum / user.taskNum
                self.cost = user.taskReward * user.continuousNum / user.taskNum
                if self.budget <= 0:
                    self.budget = 0
                    '''
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
                if self.budget > 0 and user.taskNum == 0:
                    if user.task.currentArm < user.task.arm_num:
                        self.explore(user)
                        self.calReward(user)
                    else:
                        self.allocateTask(user)
                        self.calReward()
                user.takeAction(self)
                self.updateArm(user)
                Loss += self.checkAction(user)
                engaged += user.engagementDegree
            self.status = engaged / len(self.userList)
            self.loss.append(Loss)
            self.engagedRate.append(self.status)
