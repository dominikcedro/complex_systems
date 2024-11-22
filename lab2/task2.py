"""
author: Dominik Cedro
date: 20.11.2024
description: Code solution for task 4, lab 2 of complex systems 2024/2025
"""
import numpy as np
import matplotlib.pyplot as plt
from icecream import ic

def system1(x, y):
    return y, -x

def system2(x, y):
    return y, -np.sin(x)

def system3(x, y):
    return y, -x + x**3

def system4(x, y):
    return y, x - x**3

def midpoint_method(f, x0, y0, t0, t_end, delta_t):
    t_values = np.arange(t0, t_end, delta_t)
    x_values = np.zeros(len(t_values))
    y_values = np.zeros(len(t_values))
    x_values[0] = x0
    y_values[0] = y0

    for i in range(1, len(t_values)):
        try:
            kx, ky = f(x_values[i-1], y_values[i-1])
            kx *= delta_t
            ky *= delta_t
            x_mid = x_values[i-1] + kx / 2
            y_mid = y_values[i-1] + ky / 2
            kx_mid, ky_mid = f(x_mid, y_mid)
            x_values[i] = x_values[i-1] + delta_t * kx_mid
            y_values[i] = y_values[i-1] + delta_t * ky_mid
            if np.isnan(x_values[i]) or np.isnan(y_values[i]):
                ic(f"NaN encountered at step {i}: x={x_values[i]}, y={y_values[i]}")
                break
        except OverflowError:
            x_values[i] = np.nan
            y_values[i] = np.nan
            ic(f"OverflowError at step {i}: x={x_values[i]}, y={y_values[i]}")
            break
        except ValueError:
            x_values[i] = np.nan
            y_values[i] = np.nan
            ic(f"ValueError at step {i}: x={x_values[i]}, y={y_values[i]}")
            break

    return t_values, x_values, y_values

def plot_phase_portraits(system, x0s, y0s, t0, t_end, delta_t, k):
    for x0 in x0s:
        for y0 in y0s:
            t_values, x_values, y_values = midpoint_method(system, x0, y0, t0, t_end, delta_t)
            plt.plot(x_values, y_values, alpha=0.7)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Phase Portrait for system {k}')
    plt.grid(True)
    plt.show()

x0s = np.linspace(-0.5, 0.5, 5)  # Reduced range
y0s = np.linspace(-0.5, 0.5, 5)
t0 = 0
t_end = 5  # Reduced time
delta_t = 0.001

systems = [system1, system2, system3, system4]
for i, system in enumerate(systems, 1):
    plt.figure()
    plot_phase_portraits(system, x0s, y0s, t0, t_end, delta_t,i)
    plt.show()