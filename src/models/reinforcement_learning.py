# models/reinforcement_learning.py

import numpy as np
import random
import joblib

class QLearningAgent:
    def __init__(self, state_size: int, action_size: int, learning_rate: float = 0.1, discount_factor: float = 0.95, exploration_rate: float = 1.0, exploration_decay: float = 0.995, min_exploration_rate: float = 0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        self.q_table = np.zeros((state_size, action_size))

    def choose_action(self, state: int):
        """Choose an action based on the exploration-exploitation trade-off."""
        if np.random.rand() < self.exploration_rate:
            return random.randint(0, self.action_size - 1)  # Explore
        return np.argmax(self.q_table[state])  # Exploit

    def learn(self, state: int, action: int, reward: float, next_state: int):
        """Update the Q-table based on the action taken and the reward received."""
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_delta = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_delta

    def update_exploration_rate(self):
        """Decay the exploration rate after each episode."""
        if self.exploration_rate > self.min_exploration_rate:
            self.exploration_rate *= self.exploration_decay

    def save_model(self, filename: str):
        """Save the Q-table to a file."""
        joblib.dump(self.q_table, filename)

    def load_model(self, filename: str):
        """Load the Q-table from a file."""
        self.q_table = joblib.load(filename)

# Example usage:
if __name__ == "__main__":
    state_size = 10  # Example state size
    action_size = 4  # Example action size
    agent = QLearningAgent(state_size, action_size)

    # Simulate training process
    for episode in range(1000):
        state = random.randint(0, state_size - 1)  # Random initial state
        done = False
        while not done:
            action = agent.choose_action(state)
            next_state = (state + action) % state_size  # Example transition
            reward = 1 if next_state == state_size - 1 else 0  # Example reward
            agent.learn(state, action, reward, next_state)
            state = next_state
            done = (state == state_size - 1)  # Example termination condition

        agent.update_exploration_rate()

    # Save the trained model
    agent.save_model("q_learning_model.joblib")

    # Load the model
    loaded_agent = QLearningAgent(state_size, action_size)
    loaded_agent.load_model("q_learning_model.joblib")
