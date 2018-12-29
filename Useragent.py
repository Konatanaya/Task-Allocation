import random
import math

epsilon = 0.1


class UserAgent:
    preference = []
    action = -1
    continuousNum = 0
    taskNum = 0
    taskReward = 0

    def __init__(self, id, preNum):
        self.id = id
        for index in range(preNum):
            self.preference.append(random.random())

    def printID(self, id1):
        self.id = id1
        print(self.preference)
        a = b + 1

    def takeAction(self, time):
        newPreference = []
        for pre in self.preference:
            newPreference.append(pre)
        newPreference[0] += self.calculateTemporaryPre(time)
        if random.random() < epsilon:
            self.action = random.randint(0, len(newPreference) - 1)
        else:
            self.action = newPreference.index(max(newPreference))

    def calculateTemporaryPre(self, time):
        tempPre = self.taskReward * math.exp(self.continuousNum - time)
        return tempPre

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
