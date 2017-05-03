"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand


class QLearner(object):
    def __init__(self, \
                 num_states=100, \
                 num_actions=4, \
                 alpha=0.2, \
                 gamma=0.9, \
                 rar=0.5, \
                 radr=0.99, \
                 dyna=0, \
                 verbose=False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.num_states = num_states
        self.s = 0
        self.a = 0
        self.rar = rar
        self.alpha = alpha
        self.gamma = gamma
        self.radr = radr
        self.dyna = dyna
        self.Q = np.random.rand(num_states, num_actions)
        self.T = []

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        if rand.random() < self.rar:
            self.a = rand.randint(0, (self.num_actions - 1))
            return self.a
        else:
            self.a = np.argmax(self.Q[s, :])
            return self.a



            # action = rand.randint(0, self.num_actions-1)
            # if self.verbose: print "s =", s,"a =",action
            # return

    def query(self, s_prime, r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        if rand.random() < self.rar:
            self.a = rand.randint(0, (self.num_actions - 1))
            a_prime = np.argmax(self.Q[s_prime, :])
            self.Q[self.s, self.a] = (1 - self.alpha) * self.Q[self.s, self.a] + self.alpha * (
            r + self.gamma * (self.Q[s_prime, a_prime]))
            self.rar = self.rar * self.radr
            self.T.append([self.s, self.a, s_prime, r])
            self.s = s_prime
            self.a = a_prime
            if self.dyna > 0:
                i = 0
                while i < self.dyna:
                    model = rand.choice(self.T)
                    self.Q[model[0], model[1]] = (1 - self.alpha) * self.Q[model[0], model[1]] + self.alpha * (
                    model[3] + self.gamma * (self.Q[model[2], np.argmax(self.Q[model[2], :])]))
                    i = i + 1
            return self.a



        else:
            self.a = np.argmax(self.Q[self.s, :])
            a_prime = np.argmax(self.Q[s_prime, :])
            self.Q[self.s, self.a] = (1 - self.alpha) * self.Q[self.s, self.a] + self.alpha * (
            r + self.gamma * (self.Q[s_prime, a_prime]))
            self.rar = self.rar * self.radr
            self.T.append([self.s, self.a, s_prime, r])
            self.s = s_prime
            self.a = a_prime
            if self.dyna > 0:
                i = 0
                while i < self.dyna:
                    model = rand.choice(self.T)
                    self.Q[model[0], model[1]] = (1 - self.alpha) * self.Q[model[0], model[1]] + self.alpha * (
                    model[3] + self.gamma * (self.Q[model[2], np.argmax(self.Q[model[2], :])]))
                    i = i + 1
            return self.a

            # action = rand.randint(0, self.num_actions-1)
            # if self.verbose: print "s =", s_prime,"a =",action,"r =",r
            # return


if __name__ == "__main__":
    print "Remember Q from Star Trek? Well, this isn't him"