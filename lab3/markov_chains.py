import numpy as np
import matplotlib.pyplot as plt

# 1. Эргодическая марковская цепь с 4 состояниями
states = ['A', 'B', 'C', 'D']

# 2. Матрица переходных вероятностей
P = np.array([
    [0.5, 0.5, 0.0, 0.0],  # A
    [0.3, 0.3, 0.4, 0.0],  # B
    [0.0, 0.2, 0.3, 0.5],  # C
    [0.0, 0.0, 0.6, 0.4]   # D
])

# 3. Функция моделирования цепи
def simulate_markov_chain(initial_vec, P, epsilon=1e-6, max_steps=1000):
    old_vec = np.array(initial_vec)
    history = [old_vec.copy()]
    rmse_history = []
    
    for _ in range(max_steps):
        new_vec = old_vec @ P
        rmse = np.sqrt(np.mean((new_vec - old_vec)**2))
        rmse_history.append(rmse)
        
        if rmse < epsilon:
            break
            
        old_vec = new_vec.copy()
        history.append(old_vec)
        
    return np.array(history), rmse_history

# Начальные векторы
initial_vectors = [
    np.array([1, 0, 0, 0]),    # v₁
    np.array([0, 0, 0, 1]),    # v₂
    np.array([0.25, 0.25, 0.25, 0.25])  # v₃
]

# Моделирование для всех начальных векторов
results = []
for vec in initial_vectors:
    hist, rmse = simulate_markov_chain(vec, P)
    results.append((hist, rmse))

# 4. Построение графиков
plt.figure(figsize=(15, 10))
colors = ['blue', 'green', 'red', 'purple']

# Графики компонент вектора
for i, (hist, rmse) in enumerate(results):
    plt.subplot(2, 3, i+1)
    for state in range(4):
        plt.plot(hist[:, state], color=colors[state], label=states[state])
    plt.title(f'Начальный вектор {i+1}')
    plt.xlabel('Шаг')
    plt.ylabel('Вероятность')
    plt.legend()
    plt.grid()

# Графики среднеквадратичного отклонения
plt.subplot(2, 1, 2)
for i, (_, rmse) in enumerate(results):
    plt.plot(rmse, label=f'Начальный вектор {i+1}')
plt.title('Среднеквадратичное отклонение')
plt.xlabel('Шаг')
plt.ylabel('СКО')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# 5. Аналитическое стационарное распределение
n_states = 4
A = P.T - np.eye(n_states)
A[-1, :] = 1  # Условие нормировки
b = np.zeros(n_states)
b[-1] = 1

stationary = np.linalg.solve(A, b)
print(f'Аналитическое стационарное распределение:\n {stationary.round(4)}')

# 6. Сравнение результатов
print('\nСравнение с моделированием:')
for i, (hist, _) in enumerate(results):
    simulated = hist[-1].round(4)
    diff = np.abs(simulated - stationary).sum()
    print(f'Вектор {i+1}: {simulated} | Разница: {diff:.4f}')