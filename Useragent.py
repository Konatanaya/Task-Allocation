import random
import math
import numpy as np

epsilon = 0.1


class task:
    arm_num = 10

    def __init__(self):
        self.values = [0.0 for _ in range(self.arm_num)]
        self.counts = [0 for _ in range(self.arm_num)]
        self.costs = [0.0 for _ in range(self.arm_num)]
        self.currentArm = 0

    def updateExplore(self, arm, reward, cost):
        self.costs[arm] += (cost - self.costs[arm]) / self.counts[arm]
        self.values[arm] += (reward - self.values[arm]) / self.counts[arm]

    def updateCount(self, arm):
        self.counts[arm] += 1

class UserAgent:
    def __init__(self, id, preNum):
        self.id = id
        self.preference = []
        self.action = -1
        self.continuousNum = 0
        self.taskNum = 0
        self.taskReward = 0.0
        self.task = task()
        self.engagementDegree = 0.0
        self.beta = 0.1
        self.fail = 1
        self.success = 1
        self.currentFeed = 0.0
        for index in range(preNum):
            self.preference.append(random.random())
            # self.preference[0]=0.0

    def reset(self):
        self.action = -1
        self.task = task()
        self.continuousNum = 0
        self.taskNum = 0
        self.taskReward = 0.0
        self.engagementDegree = 0.0
        self.fail = 1
        self.success = 1
        self.currentFeed = 0.0

    def printID(self, id1):
        self.id = id1
        print(self.preference)

    def takeAction(self, approach):
        '''
        if approach.budget < self.taskReward:
            self.taskReward = 0.0
            self.taskNum = 0
            self.continuousNum = 0
        '''
        newPreference = []
        for pre in self.preference:
            newPreference.append(pre)
            index = self.preference.index(pre)
            if index == 0:
                newPreference[index] += self.calculateTemporaryPre(self.continuousNum + 1, self.taskNum)
            else:
                newPreference[index] -= self.calculateTemporaryPre(self.continuousNum, self.taskNum)
                if newPreference[index] < 0:
                    newPreference[index] = 0.0

        self.action = self.chooseAction(newPreference)
        if self.action == 0 and self.taskNum != 0:
            self.continuousNum += 1
        else:
            ''''
            if approach.budget > 0 and self.taskNum != 0:
                approach.calculateReward(self)
            '''
            self.continuousNum = 0

    def chooseAction(self, newPreference):
        s = sum(newPreference)
        # return newPreference.index(max(newPreference))
        rand = random.random()
        fenzi = 0.0
        for index in newPreference:
            fenzi += index
            if rand < fenzi / s:
                return newPreference.index(index)

    def calculateTemporaryPre(self, c, d):
        tempPre = self.taskReward * math.exp(0.1*(c-d))
        return tempPre

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
