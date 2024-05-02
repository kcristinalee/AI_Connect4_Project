import numpy as np
import tensorflow as tf
import random

ROWS = 8
COLUMNS = 8
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2

# Define hyperparameters
EPISODES = 10000
GAMMA = 0.99  # Discount factor for future rewards
EPSILON_START = 1.0  # Initial exploration rate
EPSILON_END = 0.01  # Final exploration rate
EPSILON_DECAY = 0.995  # Decay rate for exploration rate
LEARNING_RATE = 0.001  # Learning rate for the optimizer
TARGET_UPDATE_FREQ = 1000  # Frequency to update target model

# Define the Deep Q-Learning agent
class DQLAgent:
    def __init__(self, state_shape=(ROWS, COLUMNS, 3), action_size=COLUMNS):
        self.state_shape = state_shape
        self.action_size = action_size
        self.epsilon = EPSILON_START
        self.model = self.build_model()  # Initialize Q-value approximation model
        self.target_model = self.build_model()  # Initialize target model for updating
        self.target_model.set_weights(self.model.get_weights())  # Copy weights to target model
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)  # Set optimizer

    def build_model(self):
        # Define the neural network model architecture
        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=self.state_shape),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dense(self.action_size, activation='linear')  # Output layer for Q-values
        ])
        model.compile(loss='mse', optimizer=self.optimizer)  # Compile the model with MSE loss
        return model

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)  # Explore by choosing a random action
        q_values = self.model.predict(state)  # Get Q-values from the model
        return np.argmax(q_values[0])  # Exploit by choosing the action with the highest Q-value

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())  # Update target model weights
