import os
import pickle
from blackjackenv import BlackjackEnv
from qlearningagent import QLearningAgent


def train_agent(env, agent, episodes, start_episode=0):
    for episode in range(start_episode, start_episode + episodes):
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
            print(f"Episode {episode}/{start_episode + episodes}")
            # Print Q-values for some state to check learning
            # Example state: player value 14, dealer visible 10, 0 aces
            some_state = (14, 10, 0)
            print(
                f"Q-values for state {some_state}: {agent.q_table[some_state]}")

        # Save the Q-table periodically
        if episode % 5000 == 0:
            with open('q_table_incremental.pkl', 'wb') as f:
                q_table = agent.get_q_table()
                pickle.dump(q_table, f)


def validate_agent(env, agent, num_games=1000):
    results = {"Player": 0, "Dealer": 0, "Draw": 0}
    for _ in range(num_games):
        env.reset_game()
        env.start_new_round()
        state = env.get_state()
        while not env.state["game_over"]:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            next_state_values = env.get_state() if not done else None
            state = next_state_values
        winner = env.state["winner"]
        if winner:
            results[winner] += 1
        else:
            results["Draw"] += 1
    return results


def incremental_training(episodes_per_increment=10000, total_iterations=10):
    actions = ["draw", "stand"]
    env = BlackjackEnv()

    # Check if there is an existing Q-table to load
    if os.path.exists('q_table_incremental.pkl'):
        with open('q_table_incremental.pkl', 'rb') as f:
            q_table = pickle.load(f)
        agent = QLearningAgent(actions)
        agent.q_table = q_table
        print("Loaded existing Q-table.")
    else:
        agent = QLearningAgent(actions, alpha=0.06164186054546666,
                               gamma=0.7979664094869481, epsilon=0.11165427144228494)
        print("Initialized new Q-table.")

    for iteration in range(total_iterations):
        print(
            f"Starting training iteration {iteration + 1}/{total_iterations}")
        start_episode = iteration * episodes_per_increment
        train_agent(env, agent, episodes_per_increment,
                    start_episode=start_episode)

        # Validate the agent after each increment
        validation_results = validate_agent(env, agent, num_games=1000)
        win_rate = validation_results["Player"] / \
            sum(validation_results.values())
        print(
            f"Validation Results after iteration {iteration + 1}: {validation_results}")
        print(f"AI Win Rate: {win_rate:.2f}")

        # Save the Q-table after each increment
        with open('q_table_incremental.pkl', 'wb') as f:
            q_table = agent.get_q_table()
            pickle.dump(q_table, f)


incremental_training(episodes_per_increment=10000, total_iterations=10)
