"""
author: Dominik Cedro
date: 08.12.2024
description: Main program for percolation laboratory list of tasks.
"""
import numpy as np
import random
import matplotlib.pyplot as plt
# from icecream import ic
import os


def create_lattice(size_of_lattice, site_p, ranom_seed = 0):
    """

    :param ranom_seed:
    :param size_of_lattice:
    :param site_p:
    :return: lattice: (np.array)
    """
    if ranom_seed:
        random.seed(ranom_seed)

    lattice = []

    for row in range(size_of_lattice):
        a = []
        for column in range(size_of_lattice):

            random_r = random.uniform(0.0, 1.0)
            if random_r < site_p:
                a.append(int(1))
            else:
                a.append(int(0))
        lattice.append(a)
    lattice = np.array(lattice)
    # print(lattice)
    return lattice


def plot_lattice(lattice):
    plt.imshow(lattice, interpolation='none')
    plt.colorbar(label='Site Occupation')
    plt.title('Lattice Occupation')
    plt.xlabel('Column')
    plt.ylabel('Row')
    plt.show()

# plot_lattice(lattice)
# plot_lattice(lattice)

##### BURNING METHOD

import numpy as np

def burning_method(lattice_raw):
    lattice = np.copy(lattice_raw)
    t_value = 2

    for index, site in enumerate(lattice[0]):
        if site == 1:
            lattice[0][index] = t_value

    while True:
        new_burns = False
        for row in range(len(lattice)):
            for col in range(len(lattice[row])):
                if lattice[row][col] == t_value:
                    # Check North
                    if row > 0 and lattice[row - 1][col] == 1:
                        lattice[row - 1][col] = t_value + 1
                        new_burns = True
                    # Check East
                    if col < len(lattice[row]) - 1 and lattice[row][col + 1] == 1:
                        lattice[row][col + 1] = t_value + 1
                        new_burns = True
                    # Check South
                    if row < len(lattice) - 1 and lattice[row + 1][col] == 1:
                        lattice[row + 1][col] = t_value + 1
                        new_burns = True
                    # Check West
                    if col > 0 and lattice[row][col - 1] == 1:
                        lattice[row][col - 1] = t_value + 1
                        new_burns = True
        if np.any(lattice[-1] == t_value + 1):
            break
        if not new_burns:
            break
        t_value += 1

    return lattice

def plot_lattice_with_values(lattice):
    plt.imshow(lattice, interpolation='none', cmap='viridis')
    plt.colorbar(label='Site Occupation')
    plt.title('Lattice Occupation')
    plt.xlabel('Column')
    plt.ylabel('Row')

    rows, cols = lattice.shape
    for i in range(rows):
        for j in range(cols):
            plt.text(j, i, str(lattice[i, j]), ha='center', va='center', color='white')

    plt.show()

# HOSHEN - KOPELMAN ALGORITHM

from collections import Counter

def hoshen_kopelman(lattice_raw):
    k = 2
    lattice = np.copy(lattice_raw)
    cluster_sizes = {}

    for row in range(len(lattice)):
        for column in range(len(lattice[row])):
            if lattice[row][column] == 1:
                top = lattice[row-1][column] if row > 0 else 0
                left = lattice[row][column-1] if column > 0 else 0

                if top == 0 and left == 0:
                    lattice[row][column] = k
                    cluster_sizes[k] = 1
                    k += 1
                elif top > 0 and left == 0:
                    lattice[row][column] = top
                    cluster_sizes[top] += 1
                elif top == 0 and left > 0:
                    lattice[row][column] = left
                    cluster_sizes[left] += 1
                elif top > 0 and left > 0:
                    if top == left:
                        lattice[row][column] = top
                        cluster_sizes[top] += 1
                    else:
                        lattice[row][column] = min(top, left)
                        cluster_sizes[min(top, left)] += cluster_sizes[max(top, left)] + 1
                        cluster_sizes[max(top, left)] = -min(top, left)

    for k in range(2, max(cluster_sizes.keys()) + 1):
        if cluster_sizes[k] > 0:
            cluster_sizes[k] = sum(1 for v in cluster_sizes.values() if v == k)

    for key in cluster_sizes:
        cluster_sizes[key] = int(cluster_sizes[key])
    # ic(cluster_sizes)
    distribution = Counter(cluster_sizes)

    return lattice, cluster_sizes, max(cluster_sizes), distribution


def write_ave_output_to_file(L, T, pf_low, avg_smax):
    os.makedirs('output', exist_ok=True)
    filename = f"output/Ave-L{L}T{T}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        for p in pf_low:
            file.write(f"{p}  {pf_low[p]}  {avg_smax[p]}\n")

def write_dist_output_to_file(L, T, cluster_distribution):
    os.makedirs('output', exist_ok=True)
    for p, distribution in cluster_distribution.items():
        filename = f"output/Dist-p{round(p,2)}L{L}T{T}.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            for size, count in distribution.items():
                file.write(f"{size}  {count}\n")

def read_input_parameters(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        params = {}
        for line in lines:
            key, value = line.split('%')
            params[key.strip()] = float(value.strip())
    return params

if __name__ == "__main__":
    lattice_size_ex1 = 10
    percolation_p_ex1 = [0.6]
    for p in percolation_p_ex1:
        lattice_raw = create_lattice(lattice_size_ex1, p,10)
        plot_lattice_with_values(lattice_raw)
        lattice_burning = burning_method(lattice_raw)
        plot_lattice_with_values(lattice_burning)
    # params = read_input_parameters('perc_ini.txt')
    # L = int(params['L'])
    # T = int(params['T'])
    # p_0 = params['p0']
    # p_k = params['pk']
    # d_p = params['dp']
    #
    # pf_low = {}
    # avg_smax = {}
    # cluster_distribution = {}
    #
    # p_values = np.arange(p_0, p_k + d_p, d_p)
    # for p in p_values:
    #     pf_count = 0
    #     smax_total = 0
    #     distribution_total = Counter()
    #
    #     for _ in range(T):
    #         lattice = create_lattice(L, p)
    #         lattice_hoshen, cluster_sizes, max_cluster_size, distribution = hoshen_kopelman(lattice)
    #
    #         if np.any(lattice_hoshen[0, :] == lattice_hoshen[-1, :]):
    #             pf_count += 1
    #
    #         smax_total += max_cluster_size
    #         distribution_total.update(distribution)
    #
    #     pf_low[p] = pf_count / T
    #     avg_smax[p] = smax_total / T
    #     cluster_distribution[p] = dict(distribution_total)
    #
    # write_ave_output_to_file(L, T, pf_low, avg_smax)
    # write_dist_output_to_file(L, T, cluster_distribution)

