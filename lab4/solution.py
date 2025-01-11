"""
author: Dominik Cedro
date: 08.12.2024
description: Main functions for percolation laboratory list of tasks.
"""
import random
import time

import matplotlib.pyplot as plt
from icecream import ic
import os
from collections import Counter
import numpy as np
from collections import defaultdict

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
    connection = np.any(lattice[-1] > 1)
    # ic(int(connection))
    return lattice, connection


import matplotlib.pyplot as plt
import numpy as np

def plot_lattice_with_values(lattice, file_name="", save=False, color='viridis', plot_title=""):
    plt.imshow(lattice, interpolation='none', cmap=color)
    # plt.colorbar(label='Site Occupation')

    if plot_title:
        plt.title(plot_title)
    else:
        plt.title('Lattice Occupation')

    plt.xlabel('Columns')
    plt.ylabel('Rows')

    rows, cols = lattice.shape
    cmap = plt.get_cmap(color)
    norm = plt.Normalize(vmin=lattice.min(), vmax=lattice.max())

    for i in range(rows):
        for j in range(cols):
            color_value = cmap(norm(lattice[i, j]))
            brightness = 0.299 * color_value[0] + 0.587 * color_value[1] + 0.114 * color_value[2] # check for light text on dark fields and vv
            text_color = 'black' if brightness > 0.5 else 'white'
            plt.text(j, i, str(lattice[i, j]), ha='center', va='center', color=text_color)

    if save:
        plt.savefig(fname=f'plot/{file_name}.png', format='png')
        plt.show()
    else:
        plt.show()


def hoshen_kopelman(lattice):
    rows, cols = lattice.shape
    labeled_lattice = np.zeros_like(lattice, dtype=int)
    cluster_sizes = defaultdict(int)
    next_label = 2
    label_map = {}

    def find(label):
        while label_map[label] != label:
            label = label_map[label]
        return label

    def union(label1, label2):
        root1 = find(label1)
        root2 = find(label2)
        if root1 != root2:
            label_map[root2] = root1
            cluster_sizes[root1] += cluster_sizes[root2]
            del cluster_sizes[root2]

    for i in range(rows):
        for j in range(cols):
            if lattice[i, j] == 1:
                top = labeled_lattice[i - 1, j] if i > 0 else 0
                left = labeled_lattice[i, j - 1] if j > 0 else 0

                if top == 0 and left == 0:
                    labeled_lattice[i, j] = next_label
                    cluster_sizes[next_label] = 1
                    label_map[next_label] = next_label
                    next_label += 1
                elif top > 0 and left == 0:
                    labeled_lattice[i, j] = top
                    cluster_sizes[top] += 1
                elif left > 0 and top == 0:
                    labeled_lattice[i, j] = left
                    cluster_sizes[left] += 1
                elif top > 0 and left > 0:
                    if top == left:
                        labeled_lattice[i, j] = top
                        cluster_sizes[top] += 1
                    else:
                        labeled_lattice[i, j] = min(top, left)
                        union(top, left)
                        cluster_sizes[find(top)] += 1

    for i in range(rows):
        for j in range(cols):
            if labeled_lattice[i, j] > 0:
                labeled_lattice[i, j] = find(labeled_lattice[i, j])

    final_cluster_sizes = {k: v for k, v in cluster_sizes.items() if v > 0}

    distribution = defaultdict(int)
    for size in final_cluster_sizes.values():
        distribution[size] += 1

    return labeled_lattice, list(final_cluster_sizes.values()), max(final_cluster_sizes.values()) if final_cluster_sizes else 0, dict(distribution)

def write_ave_output_to_file(L, T, pf_low, avg_smax):
    os.makedirs('output', exist_ok=True)
    filename = f"output/Ave-L{L}T{T}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        for p in pf_low:
            file.write(f"{round(p,2)}  {pf_low[p]}  {avg_smax[p]}\n")


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


def read_ave_file(filename):
    data = np.loadtxt(filename)
    p_values = data[:, 0]
    pf_low = data[:, 1]
    return p_values, pf_low


def read_dist_file(filename):
    c_size = []
    c_count = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            c_size.append(int(parts[0]))
            c_count.append(int(parts[1]))

    return np.array(c_size), np.array(c_count)
