import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

maze_size = 4

# Wall-based maze representation: [Top, Right, Bottom, Left]
maze = [
    [[1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 0, 0], [1, 1, 1, 0]],
    [[0, 1, 0, 1], [1, 0, 0, 1], [0, 0, 1, 0], [1, 1, 0, 0]],
    [[0, 1, 1, 1], [0, 0, 0, 1], [0, 1, 1, 0], [0, 1, 0, 1]],
    [[1, 0, 1, 1], [0, 0, 1, 0], [1, 0, 1, 0], [0, 1, 1, 0]]]

start = [0, 0]
goal = [3, 3]

actions = ['up', 'right', 'down', 'left']
Q = {}

def move(position, action):
    x, y = position
    wall = maze[x][y]

    if action == 'up' and wall[0] == 0 and x > 0:
        x = x- 1
    elif action == 'right' and wall[1] == 0 and y < maze_size - 1:
        y = y+ 1
    elif action == 'down' and wall[2] == 0 and x < maze_size - 1:
        x = x + 1
    elif action == 'left' and wall[3] == 0 and y > 0:
        y = y - 1
    else:
        return [position[0], position[1]], -5  # penalty for hitting wall

    if [x, y] == goal:
        return [x, y], 10  # goal reached award 10 points
    else:
        return [x, y], -1  # normal move cost

def get_q(state, action):
    return Q.get((tuple(state), action), 0.0)

def update_q(state, action, reward, next_state, alpha=0.1, gamma=0.9):
    max_next_q = max([get_q(next_state, a) for a in actions])
    current_q = get_q(state, action)
    new_q = current_q + alpha * (reward + gamma * max_next_q - current_q) #alpha --> How fast you learn
                                                                          #gamma --> How far ahead you plan
    Q[(tuple(state), action)] = new_q

def choose_action(state, epsilon = max(0.1, 0.9 * (0.99 ** episode)) ): # decay over time, learning faster, explores early, exploit later.
    if random.random() < epsilon:
        return random.choice(actions)
    else:
        q_values = {a: get_q(state, a) for a in actions}
        max_q = max(q_values.values())
        best_actions = [a for a, q in q_values.items() if q == max_q]
        return random.choice(best_actions)

# Training
episodes = 500
max_steps = 50

for episode in range(episodes):
    state = start
    for _ in range(max_steps):
        action = choose_action(state)
        next_state, reward = move(state, action)
        update_q(state, action, reward, next_state)
        state = next_state
        if state == goal:
            break

# Testing to get path
def test_run(start, goal, max_steps=50):
    state = start
    path = [state]
    for _ in range(max_steps):
        q_values = {a: get_q(state, a) for a in actions}
        max_q = max(q_values.values())
        best_actions = [a for a, q in q_values.items() if q == max_q]
        action = random.choice(best_actions)
        next_state, reward = move(state, action)
        path.append(next_state)
        state = next_state
        if state == goal:
            break
    return path

path = test_run(start, goal)

# Visualization
def visualize_maze(path):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, maze_size)
    ax.set_ylim(0, maze_size)
    ax.invert_yaxis()
    ax.set_xticks(np.arange(maze_size + 1))
    ax.set_yticks(np.arange(maze_size + 1))
    ax.grid(True)

    # Draw walls
    for x in range(maze_size):
        for y in range(maze_size):
            walls = maze[x][y]
            if walls[0]:  # Top
                ax.plot([y, y + 1], [x, x], color='black', linewidth=2)
            if walls[1]:  # Right
                ax.plot([y + 1, y + 1], [x, x + 1], color='black', linewidth=2)
            if walls[2]:  # Bottom
                ax.plot([y, y + 1], [x + 1, x + 1], color='black', linewidth=2)
            if walls[3]:  # Left
                ax.plot([y, y], [x, x + 1], color='black', linewidth=2)

    # Start and Goal
    ax.text(start[1] + 0.5, start[0] + 0.5, 'S', color='green', ha='center', va='center', fontsize=12)
    ax.text(goal[1] + 0.5, goal[0] + 0.5, 'G', color='red', ha='center', va='center', fontsize=12)

    # Mouse
    mouse_dot, = ax.plot([], [], 'bo', markersize=12)

    def update(frame):
        pos = path[frame]
        mouse_dot.set_data([pos[1] + 0.5], [pos[0] + 0.5])  # FIXED: Wrapped in list
        return mouse_dot,

    ani = animation.FuncAnimation(fig, update, frames=len(path), interval=500, blit=True, repeat=False)
    plt.show()

visualize_maze(path)
