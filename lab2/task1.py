"""
author: Dominik Cedro
date: 18.10.2024
description: This is solution to task 1 from non linear dynamics lab
"""
import scipy
import numpy as np
import matplotlib.pyplot as plt


def function_f(x):
    return x * (x - 1) * (x - 2)


def f_prime(x):
    return 3 * x ** 2 - 6 * x + 2


def calc_derivative(x):
    return scipy.misc.derivative(function_f, x,dx=1e-7) # include small step


fixed_points = [x * 0.1 for x in range(-100, 101)]
stability = {x: f_prime(x) for x in fixed_points}

list_of_points =[]
print("the ther one")
for point, derivative in stability.items():
    if derivative < 0:
        print(f"Stable fixed point: {round(point,1)}")
        list_of_points.append(round(point,1))


def euler_method(function_f, x0, t0, t_end, delta_t):
    t_values = np.arange(t0, t_end, delta_t)
    x_values = np.zeros(len(t_values))
    x_values[0] = x0

    for i in range(1, len(t_values)):
        x_values[i] = x_values[i - 1] + delta_t * function_f(x_values[i - 1])

    return t_values, x_values


x0s = list_of_points
t0 = 0
t_end = 10
delta_t = 0.1
for x0 in x0s:
    t_values, x_values = euler_method(function_f, x0, t0, t_end, delta_t)
    plt.plot(t_values, x_values, label=f'x0={x0}, dt={delta_t}')

plt.xlabel('Time')
plt.ylabel('x')
plt.title('Numerical Solution of dx/dt = x(x-1)(x-2)')
# plt.legend()
plt.grid(True)
plt.show()
