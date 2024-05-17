import random
import pickle
from blackjackenv import BlackjackEnv
from qlearningagent import QLearningAgent


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


def random_search(num_iterations):
    best_win_rate = 0
    best_params = None
    results = []

    for _ in range(num_iterations):
        alpha = random.uniform(0.01, 0.9)
        gamma = random.uniform(0.5, 0.99)
        epsilon = random.uniform(0.01, 0.3)

        print(f"Training with alpha={alpha}, gamma={gamma}, epsilon={epsilon}")
        actions = ["draw", "stand"]
        env = BlackjackEnv()
        agent = QLearningAgent(actions, alpha=alpha,
                               gamma=gamma, epsilon=epsilon)

        # Train the agent
        train_agent(env, agent, 50000)

        # Validate the agent
        validation_results = validate_agent(env, agent, num_games=1000)
        win_rate = validation_results["Player"] / \
            sum(validation_results.values())

        print(f"Validation Results: {validation_results}")
        print(f"Win Rate: {win_rate:.2f}")

        results.append((alpha, gamma, epsilon, win_rate))

        if win_rate > best_win_rate:
            best_win_rate = win_rate
            best_params = (alpha, gamma, epsilon)

    print(
        f"Best Parameters: alpha={best_params[0]}, gamma={best_params[1]}, epsilon={best_params[2]}")
    print(f"Best Win Rate: {best_win_rate:.2f}")

    # Save the best model
    with open('q_table_best.pkl', 'wb') as f:
        q_table = agent.get_q_table()
        pickle.dump(q_table, f)


random_search(num_iterations=50)
