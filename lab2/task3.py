"""
author: Dominik Cedro
date: 17.11.2024
description: Code solution for task 3, lab 2 of complex systems 2024/2025
"""
import numpy as np
import matplotlib.pyplot as plt

matrices = { # maybe numpy?
    'a': np.array([[-2, 1], [0, 2]]),
    'b': np.array([[3, -4], [2, -1]]),
    'c': np.array([[-3, -2], [-1, -3]]),
    'd': np.array([[2, 0], [0, 2]])
}

def system(A, x, y):
    dx = A[0, 0] * x + A[0, 1] * y
    dy = A[1, 0] * x + A[1, 1] * y
    return dx, dy

def midpoint_method(A, x0, y0, t0, t_end, delta_t):
    t_values = np.arange(t0, t_end, delta_t)
    x_values = np.zeros(len(t_values))
    y_values = np.zeros(len(t_values))
    x_values[0] = x0
    y_values[0] = y0

    for i in range(1, len(t_values)):
        kx, ky = system(A, x_values[i-1], y_values[i-1])
        kx *= delta_t
        ky *= delta_t
        x_mid = x_values[i-1] + kx / 2
        y_mid = y_values[i-1] + ky / 2
        kx_mid, ky_mid = system(A, x_mid, y_mid)
        x_values[i] = x_values[i-1] + delta_t * kx_mid
        y_values[i] = y_values[i-1] + delta_t * ky_mid

    return t_values, x_values, y_values

def plot_phase_portraits(A, x0s, y0s, t0, t_end, delta_t,key):
    for x0 in x0s:
        for y0 in y0s:
            t_values, x_values, y_values = midpoint_method(A, x0, y0, t0, t_end, delta_t)
            plt.plot(x_values, y_values, label=f'x0={x0}, y0={y0}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Phase Portrait for Matrix {key}')
    plt.legend()
    plt.grid(True)
    plt.show()

x0s = np.linspace(-2, 2, 5)
y0s = np.linspace(-2, 2, 5)
t0 = 0
t_end = 10
delta_t = 0.01

for key, A in matrices.items():
    plt.figure()
    plot_phase_portraits(A, x0s, y0s, t0, t_end, delta_t, key)
    det_A = np.linalg.det(A)
    tr_A = np.trace(A)
    print(f'Matrix {key}: det(A) = {det_A}, tr(A) = {tr_A}')