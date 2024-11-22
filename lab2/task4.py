import numpy as np
import matplotlib.pyplot as plt

# Define the system of first-order differential equations
def system(x, y):
    dx = x * (3 - x - 2 * y)
    dy = y * (2 - x - y)
    return dx, dy

# Find fixed points
def find_fixed_points():
    fixed_points = []
    for x in np.linspace(0, 3, 100):
        for y in np.linspace(0, 2, 100):
            dx, dy = system(x, y)
            if abs(dx) < 1e-6 and abs(dy) < 1e-6:
                fixed_points.append((x, y))
    return fixed_points

# Midpoint method for solving the system of first-order differential equations
def midpoint_method(f, x0, y0, t0, t_end, delta_t):
    t_values = np.arange(t0, t_end, delta_t)
    x_values = np.zeros(len(t_values))
    y_values = np.zeros(len(t_values))
    x_values[0] = x0
    y_values[0] = y0

    for i in range(1, len(t_values)):
        kx, ky = f(x_values[i-1], y_values[i-1])
        kx *= delta_t
        ky *= delta_t
        x_mid = x_values[i-1] + kx / 2
        y_mid = y_values[i-1] + ky / 2
        kx_mid, ky_mid = f(x_mid, y_mid)
        x_values[i] = x_values[i-1] + delta_t * kx_mid
        y_values[i] = y_values[i-1] + delta_t * ky_mid

    return t_values, x_values, y_values
"""
author: Dominik Cedro
date: 19.11.2024
description: Code solution for task 4, lab 2 of complex systems 2024/2025
"""
def plot_phase_portraits(f, x0s, y0s, t0, t_end, delta_t):
    plt.figure(figsize=(14, 10))  # Adjust the figure size
    for x0 in x0s:
        for y0 in y0s:
            t_values, x_values, y_values = midpoint_method(f, x0, y0, t0, t_end, delta_t)
            plt.plot(x_values, y_values, label=f'x0={x0}, y0={y0}', alpha=0.7)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Phase Portrait')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)  # Legend beneath the plot
    plt.grid(True)
    plt.tight_layout()
    plt.show()

x0s = np.linspace(0.1, 2.9, 5)
y0s = np.linspace(0.1, 1.9, 5)
t0 = 0
t_end = 10
delta_t = 0.01

plot_phase_portraits(system, x0s, y0s, t0, t_end, delta_t)
fixed_points = find_fixed_points()
print("Fixed Points:", fixed_points)

def modified_system(x, y):
    dx = x * (3 - x - 2 * y)
    dy = y * (2 - x - y)
    return dx, dy

plot_phase_portraits(modified_system, x0s, y0s, t0, t_end, delta_t)