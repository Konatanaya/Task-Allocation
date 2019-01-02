import random
import math
import numpy as np

epsilon = 0.1


class task:
    arm_num = 10

    def __init__(self):
        self.values = [0.0 for _ in range(self.arm_num)]
        self.counts = [0.0 for _ in range(self.arm_num)]
        self.costs = [0.0 for _ in range(self.arm_num)]

    def update(self, arm, reward):
        self.counts[arm] += 1
        self.values[arm] += (reward - self.values[arm]) / self.counts[arm]

    def updateExplore(self, arm, reward, cost):
        self.counts[arm] += 1
        self.costs[arm] += (cost - self.costs[arm]) / self.counts[arm]
        self.values[arm] += (reward - self.values[arm]) / self.counts[arm]


class UserAgent:
    def __init__(self, id, preNum):
        self.preference = []
        self.action = -1
        self.continuousNum = 0
        self.taskNum = 0
        self.taskReward = 0.0
        self.id = id
        self.task = task()
        self.engagementDegree = 0.0
        self.beta = 0.1
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


    def printID(self, id1):
        self.id = id1
        print(self.preference)

    def takeAction(self, approach):
        if approach.budget < self.taskReward:
            self.taskReward = 0.0
            self.taskNum = 0
        newPreference = []
        for pre in self.preference:
            newPreference.append(pre)
            index = self.preference.index(pre)
            if index == 0:
                newPreference[index] += self.calculateTemporaryPre()
            else:
                newPreference[index] -= self.calculateTemporaryPre() / (len(self.preference) - 1)
                if newPreference[index] <0:
                    newPreference[index] = 0.0

        self.action = self.chooseAction(newPreference)

    def chooseAction(self, newPreference):
        s = sum(newPreference)
        # return newPreference.index(max(newPreference))
        rand = random.random()
        fenzi = 0.0
        for index in newPreference:
            fenzi += index
            if rand < fenzi / s:
                return newPreference.index(index)

    def calculateTemporaryPre(self):
        tempPre = self.taskReward * math.exp(0.1 * (self.continuousNum + 1 - self.taskNum))
        return tempPre

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
