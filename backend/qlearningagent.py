import numpy as np
from collections import defaultdict


class QLearningAgent:
    def __init__(self, actions, alpha=0.06164186054546666, gamma=0.7979664094869481, epsilon=0.11165427144228494):
        self.q_table = defaultdict(lambda: np.zeros(len(actions)))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = actions

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice(self.actions)
        else:
            state_action = self.q_table[state]
            action = self.actions[np.argmax(state_action)]
        return action

    def learn(self, state, action, reward, next_state):
        action_index = self.actions.index(action)
        predict = self.q_table[state][action_index]
        if next_state is not None:
            target = reward + self.gamma * np.max(self.q_table[next_state])
        else:
            target = reward
        self.q_table[state][action_index] += self.alpha * (target - predict)

    def get_q_table(self):
        return dict(self.q_table)
