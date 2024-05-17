import pickle
from blackjackenv import BlackjackEnv
from qlearningagent import QLearningAgent
from collections import defaultdict
import numpy as np

# Load the trained Q-Table
with open('q_table.pkl', 'rb') as f:
    q_table = pickle.load(f)

actions = ["draw", "stand"]
env = BlackjackEnv()
agent = QLearningAgent(actions)

# Set the agent's Q-Table to the loaded Q-Table
agent.q_table = defaultdict(lambda: np.zeros(len(actions)), q_table)


def play_game(env, agent):
    env.reset_game()
    env.start_new_round()
    state = env.get_state()
    while not env.state["game_over"]:
        action = agent.choose_action(state)
        next_state, reward, done = env.step(action)
        next_state_values = env.get_state() if not done else None
        state = next_state_values
    return env.state["winner"]


def validate_agent(env, agent, num_games=1000):
    results = {"Player": 0, "Dealer": 0, "Draw": 0}
    for _ in range(num_games):
        winner = play_game(env, agent)
        if winner:
            results[winner] += 1
        else:
            results["Draw"] += 1
    return results


results = validate_agent(env, agent, num_games=1000)
print(f"Validation Results over 1000 games: {results}")
win_rate = results["Player"] / sum(results.values())
print(f"AI Win Rate: {win_rate:.2f}")

# Example of single game play to see AI's actions
play_game(env, agent)
