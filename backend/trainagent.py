from blackjackenv import BlackjackEnv
from qlearningagent import QLearningAgent
import pickle


def train_agent(env, agent, episodes):
    for episode in range(episodes):
        env.reset_game()
        env.start_new_round()
        state = env.get_state()
        while not env.state["game_over"]:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            next_state_values = env.get_state() if not done else None
            agent.learn(state, action, reward, next_state_values)
            state = next_state_values
        if episode % 1000 == 0:
            print(f"Episode {episode}/{episodes}")
            # Print Q-values for some state to check learning
            # Example state: player value 14, dealer visible 10, 0 aces
            some_state = (14, 10, 0)
            print(
                f"Q-values for state {some_state}: {agent.q_table[some_state]}")


actions = ["draw", "stand"]
env = BlackjackEnv()
agent = QLearningAgent(actions, alpha=0.06164186054546666,
                       gamma=0.7979664094869481, epsilon=0.11165427144228494)
train_agent(env, agent, 1000000)

# Save the trained Q-Table
with open('q_table.pkl', 'wb') as f:
    q_table = agent.get_q_table()
    pickle.dump(q_table, f)
