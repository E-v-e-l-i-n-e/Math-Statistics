import math
import matplotlib.pyplot as plt
with open('sample.txt', "r", encoding="utf-8") as f:
    sample = [float(x) for x in f.read().split()]

n = len(sample)
sample.sort()
x_min, x_max = sample[0], sample[-1]

if n <= 10:
    k = n + 1
    bins = sorted(set(sample))
    h = 0
elif (n > 10 and n <= 200):
    # Формула Стерджеса
    k = math.ceil(1 + math.log2(n))
    h = (x_max - x_min) / k
    bins = [x_min + i * h for i in range(k + 1)]
elif n > 200:
    k =round(math.sqrt(n))
    h = (x_max - x_min) / k
    bins = [x_min + i * h for i in range(k + 1)]


print(f"n = {n}, k = {k}, h = {h:.3f}")
print("Границы:", [round(b, 4) for b in bins])


# Расчет квантили
p = float(input("Введите вероятность p (от 0 до 1): "))
while not (0 < p < 1):
    print ("Вероятность должна быть в интервале от 0 до 1")
    p = float(input("Введите вероятность p (от 0 до 1): "))

position = n * p
if position.is_integer():
    #Если n * p целое, берем полусумму соседних элементов
    idx = int(position) - 1
    quantile = (sample[idx] + sample[idx + 1]) / 2
else:
    # Иначе округляем вверх (индекс сдвигаем на -1)
    idx = math.ceil(position) - 1
    quantile = sample[idx]

print(f"Выборочная квантиль порядка {p}: {quantile}")


# построение графика
pts = bins
f_vals = [sum(val <= p for val in sample) / n for p in pts]

plt.figure(figsize=(8, 5))
margin = (x_max - x_min) * 0.2 if x_max != x_min else 1.0
plt.plot([pts[0] - margin, pts[0]], [0, 0], color='#1f77b4', linewidth=2)
plt.scatter(pts[0], 0, facecolors='white', edgecolors='#1f77b4', s=40, zorder=3)

# Ступеньки
for i in range(len(pts) - 1):
    left, right = pts[i], pts[i + 1]
    y = f_vals[i]
    plt.plot([left, right], [y, y], color='#1f77b4', linewidth=2)
    plt.scatter(left, y, color='#1f77b4', s=35, zorder=3)
    plt.scatter(right, y, facecolors='white', edgecolors='#1f77b4', s=40, zorder=3)


plt.plot([pts[-1], pts[-1] + margin], [1.0, 1.0], color='#1f77b4', linewidth=2)
plt.scatter(pts[-1], 1.0, color='#1f77b4', s=35, zorder=3)

plt.title('Выборочная функция распределения $F_n(x)$', fontsize=12)
plt.xlabel('x')
plt.ylabel('$F_n(x)$')
plt.ylim(-0.05, 1.05)
plt.yticks([i * 0.1 for i in range(11)])
plt.xlim(pts[0] - margin, pts[-1] + margin)
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()