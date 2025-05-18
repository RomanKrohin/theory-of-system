import numpy as np
import matplotlib.pyplot as plt

def next_state(current_state, rule):
    """Вычисляет следующее состояние клеточного автомата."""
    n = len(current_state)
    new_state = []
    for i in range(n):
        left = current_state[i-1] if i > 0 else 0
        current = current_state[i]
        right = current_state[i+1] if i < n-1 else 0
        
        index = left * 4 + current * 2 + right
        bit = (rule >> (7 - index)) & 1
        new_state.append(bit)
    return new_state

size = 101
iterations = 100
rule = 110

initial_state = [0] * size
initial_state[size // 2] = 1

history = [initial_state.copy()]
current = initial_state.copy()
for _ in range(iterations):
    current = next_state(current, rule)
    history.append(current)

history = np.array(history)

plt.figure(figsize=(10, 6))
plt.imshow(history, cmap='binary', interpolation='nearest')
plt.title(f'Правило {rule}')
plt.axis('off')
plt.show()