"""
author: Dominik Cedro
date: 08.12.2024
description: Main program for percolation laboratory list of tasks.
"""
import random
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


def plot_lattice(lattice):
    plt.imshow(lattice, interpolation='none')
    plt.colorbar(label='Site Occupation')
    plt.title('Lattice Occupation')
    plt.xlabel('Column')
    plt.ylabel('Row')
    plt.show()


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


def plot_lattice_with_values(lattice, title="", save=False):
    plt.imshow(lattice, interpolation='none', cmap='viridis')
    plt.colorbar(label='Site Occupation')

    if title:
        plt.title(title)
    else:
        title='plot'
        plt.title('Lattice Occupation')

    plt.xlabel('Column')
    plt.ylabel('Row')

    rows, cols = lattice.shape
    for i in range(rows):
        for j in range(cols):
            plt.text(j, i, str(lattice[i, j]), ha='center', va='center', color='white')
    if save:
        plt.savefig(fname=f'plot/{title}.png', format='png')
        plt.show()
    else:
        plt.show()


def hoshen_kopelman(lattice_raw):
    k = 2
    Mk=1
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
    distribution = Counter(cluster_sizes)

    return lattice, cluster_sizes, max(cluster_sizes), distribution


def hoshen_kopelman_2(lattice):
    """
    Perform the Hoshen-Kopelman algorithm on a given lattice.

    Args:
        lattice (2D array): Input lattice with 1s (occupied sites) and 0s (empty sites).

    Returns:
        labeled_lattice (2D array): Lattice with unique cluster labels.
        cluster_sizes (list): List of cluster sizes.
        max_cluster_size (int): Size of the largest cluster.
        distribution (dict): Histogram of cluster sizes.
    """
    # Initialize variables
    rows, cols = lattice.shape
    labeled_lattice = np.zeros_like(lattice, dtype=int)
    cluster_sizes = defaultdict(int)  # To store sizes of clusters
    next_label = 2  # Start labels from 2 (1 is reserved for occupied cells)

    # First pass: Assign labels
    for i in range(rows):
        for j in range(cols):
            if lattice[i, j] == 1:  # Only process occupied cells
                top = labeled_lattice[i - 1, j] if i > 0 else 0
                left = labeled_lattice[i, j - 1] if j > 0 else 0

                if top == 0 and left == 0:  # New cluster
                    labeled_lattice[i, j] = next_label
                    cluster_sizes[next_label] = 1
                    next_label += 1
                elif top > 0 and left == 0:  # Extend top cluster
                    labeled_lattice[i, j] = top
                    cluster_sizes[top] += 1
                elif left > 0 and top == 0:  # Extend left cluster
                    labeled_lattice[i, j] = left
                    cluster_sizes[left] += 1
                elif top > 0 and left > 0:  # Merge clusters or extend one
                    if top == left:
                        labeled_lattice[i, j] = top
                        cluster_sizes[top] += 1
                    else:  # Merge clusters
                        labeled_lattice[i, j] = min(top, left)
                        smaller, larger = min(top, left), max(top, left)
                        cluster_sizes[smaller] += cluster_sizes[larger] + 1
                        cluster_sizes[larger] = -smaller
                else:
                    raise ValueError("Unexpected case encountered.")

    # Second pass: Resolve negative masses and relabel
    for i in range(rows):
        for j in range(cols):
            if labeled_lattice[i, j] > 0:
                label = labeled_lattice[i, j]
                while cluster_sizes[label] < 0:
                    label = -cluster_sizes[label]
                labeled_lattice[i, j] = label

    # Filter cluster sizes to exclude merged ones (negative values)
    final_cluster_sizes = {k: v for k, v in cluster_sizes.items() if v > 0}

    # Build the cluster size distribution
    distribution = defaultdict(int)
    for size in final_cluster_sizes.values():
        distribution[size] += 1

    return  labeled_lattice, list(final_cluster_sizes.values()), max(final_cluster_sizes.values()) if final_cluster_sizes else 0, dict(distribution),


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


if __name__ == "__main__":
    # PART A OF TASKS - lattice, burning, hoshen
    # lattice_size_ex1 = 10
    # percolation_p_ex1 = [0.4, 0.6, 0.8]
    # for p in percolation_p_ex1:
    #     lattice_raw = create_lattice(lattice_size_ex1, p,10)
    #     plot_lattice_with_values(lattice_raw, title=f"Lattice raw {p}.png", save=True)
    #     lattice_burning, connection = burning_method(lattice_raw)
    #     plot_lattice_with_values(lattice_burning,f"Burning method p={p}", save=True)
    #     labeled_lattice, cluster_sizes, max_size, distribution = hoshen_kopelman_2(lattice_raw)
    #     plot_lattice_with_values(labeled_lattice,save=True, title=f"Hoshen_Kopelman{p}")

    # PART B, C, D OF TASKS
    params = read_input_parameters('perc_ini.txt')
    L = int(params['L'])
    T = int(params['T'])
    p_0 = params['p0']
    p_k = params['pk']
    d_p = params['dp']

    p_flow = {}
    avg_smax = {}
    cluster_distribution = {}

    p_values = np.arange(p_0, p_k + d_p, d_p)
    for p in p_values:
        pf_count = 0
        smax_total = 0
        distribution_total = Counter()

        for _ in range(T):
            lattice = create_lattice(L, p)
            lattice_burned, connection = burning_method(lattice)
            lattice_hoshen, cluster_sizes, max_cluster_size, distribution = hoshen_kopelman(lattice)

            pf_count += connection

            smax_total += max_cluster_size
            distribution_total.update(distribution)

        p_flow[p] = pf_count / T
        avg_smax[p] = smax_total / T
        cluster_distribution[p] = dict(distribution_total)

    write_ave_output_to_file(L, T, p_flow, avg_smax)
    write_dist_output_to_file(L, T, cluster_distribution)

