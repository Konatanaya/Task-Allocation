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
        self.explore = 20
        self.rate = 0.1
        self.status = 0

    def allocateTask(self, user):
        num = user.defaultDif
        if user.count_in < self.explore:
            num = 1
            user.count_in += 1
        else:
            #for index in range(user.defaultDif, 2,-1):
                if user.e_gamma < math.pow(1/num, 1/(num-1)):
                    num -= 1
                    ''''
                else:
                    num = index
                    break
                '''

        r_upper = (1 - self.status) * (num + math.log(num))
        r_lower = user.pre_dif_upper / math.pow(user.e_gamma,num-1)
        ''''
        if r_lower > r_upper and num>1:
            n_e = math.floor(math.log(user.pre_dif_upper/r_upper, user.e_gamma))
            if n_e < num:
                num = n_e
'''
        r = min(r_upper, r_lower)
        if r == r_upper:
            user.flag = 0
        else:
            user.flag = 1
        user.taskNum = num
        user.taskReward = r
        #self.budget -= user.taskReward

    def checkAction(self, user):
        n = 0
        r = 0
        if user.action == 0:
            user.engagementDegree += self.beta * (1 - user.engagementDegree)
            if user.continuousNum == user.taskNum:
                user.defaultDif = min(max(user.taskNum + 1, user.defaultDif), self.maxTask)
                if user.taskNum > 1:
                    #user.defaultDif = min(max(user.taskNum + 1, user.defaultDif), self.maxTask)
                    if user.flag == 0:
                        #user.pre_dif_upper = max(user.pre_dif_upper * (1 - self.rate), user.pre_dif_lower)
                        user.e_gamma = min(1.0, user.e_gamma * (1 + self.rate))
                    else:
                        # user.defaultDif = min(max(user.taskNum + 1, user.defaultDif), self.maxTask)
                        #user.pre_dif_upper = max(user.pre_dif_upper*(1 - self.rate), user.pre_dif_lower)
                        user.e_gamma = min(1.0, user.e_gamma * (1 + self.rate))
                elif user.taskNum == 1:
                    user.pre_dif_upper = min(user.pre_dif_upper, user.taskReward)

                self.budget -= user.taskReward
                if self.budget <= 0:
                    self.budget = 0
                user.continuousNum = 0
                user.taskNum = 0
                user.taskReward = 0
        else:

            if user.taskNum > 1:
                if user.flag == 0:
                    user.e_gamma = max(0.0, user.e_gamma * (1 - self.rate))
                    #user.e_gamma = min(1.0, user.e_gamma * (1 + self.rate))
                    #user.pre_dif_lower = max(user.pre_dif_upper, user.pre_dif_lower * (1 + self.rate))
                else:
                    #user.pre_dif_lower = max(user.pre_dif_upper, user.pre_dif_lower * (1 + self.rate))
                    user.defaultDif = max(user.taskNum - 1, 2)
                    user.pre_dif_upper = max(user.pre_dif_upper * (1 - self.rate), user.pre_dif_lower)
                    user.e_gamma = max(0.0, user.e_gamma * (1 - self.rate))

            elif user.taskNum == 1:
                user.pre_dif_lower = max(user.pre_dif_lower, user.taskReward)

            self.budget += user.taskReward
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
