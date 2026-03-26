import random
import numpy as np

class RLAgent:

    def __init__(self):

        self.q = {}

        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1

        self.actions = [0,1,2,3]

    def choose_action(self,state):

        if random.random() < self.epsilon:
            return random.choice(self.actions)

        qs=[self.q.get((state,a),0) for a in self.actions]

        return int(np.argmax(qs))

    def update(self,state,action,reward,next_state):

        old=self.q.get((state,action),0)

        next_max=max([self.q.get((next_state,a),0) for a in self.actions])

        new=old+self.alpha*(reward+self.gamma*next_max-old)

        self.q[(state,action)]=new