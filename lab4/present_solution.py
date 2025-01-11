"""
author: Dominik Cedro
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

from icecream import ic

from lab4.solution import read_ave_file, read_dist_file


def read_ave_output_file(filename):
    data = np.loadtxt(filename)
    p_values = data[:, 0]
    pf_low = data[:, 1]
    avg_smax = data[:, 2]
    return p_values, pf_low, avg_smax


# def plot_sample_configurations():
#     # Assuming the sample configurations are generated and saved as images
#     fig, axs = plt.subplots(2, 3, figsize=(15, 10))
#     for i, p in enumerate([0.4, 0.6, 0.8]):
#         img_burning = plt.imread(f'output/sample_burning_p{p}.png')
#         img_hk = plt.imread(f'output/sample_hk_p{p}.png')
#         axs[0, i].imshow(img_burning)
#         axs[0, i].set_title(f'Burning Algorithm, p={p}')
#         axs[0, i].axis('off')
#         axs[1, i].imshow(img_hk)
#         axs[1, i].set_title(f'HK Algorithm, p={p}')
#         axs[1, i].axis('off')
#     plt.tight_layout()
#     plt.show()

def plot_pf_low_vs_p():
    fig, ax = plt.subplots()
    for L in [100]:
        filename = f'output/Ave-L{L}T20.txt'
        p_values, pf_low, _ = read_ave_output_file(filename)
        ax.plot(p_values, pf_low, label=f'L={L}', marker='o')
    ax.set_xlabel('p')
    ax.set_ylabel('Pf low')
    ax.legend()
    ax.grid(True)
    plt.show()

def plot_avg_smax_vs_p():
    fig, ax = plt.subplots()
    for L in [100]:
        filename = f'output/Ave-L{L}T10.txt'
        p_values, _, avg_smax = read_ave_output_file(filename)
        ax.plot(p_values, avg_smax, label=f'L={L}', marker='s')
    ax.set_xlabel('p')
    ax.set_ylabel('Average size of the maximum cluster ⟨smax⟩')
    ax.legend()
    ax.grid(True)
    plt.show()



def plot_cluster_distribution():
    fig, axs = plt.subplots(4, 3, figsize=(15, 20))  # Adjusted to 4 rows and 3 columns
    p_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    for i, p in enumerate(p_values):
        filename = f'output/Dist-p{p}L100T20.txt'
        sizes, counts = read_dist_file(filename)
        ic(len(sizes), len(counts))
        ax = axs[i // 3, i % 3]  # Adjusted to access the correct subplot
        ax.plot(sizes, counts, label=f'p={p}', marker='^')
        ax.set_xlabel('Cluster size')
        ax.set_ylabel('Count')
        ax.legend()
        ax.grid(True)
    plt.tight_layout()
    plt.show()

def plot_p_flow_for_given_output(): # TASK B
    L_values = [10, 50, 100]
    T = 20

    for L in L_values:
        filename = f'output/Ave-L{L}T{T}.txt'
        p_values, pf_low = read_ave_file(filename)
        plt.plot(p_values, pf_low, label=f'L={L}', marker='o')

    plt.xlabel('p')
    plt.ylabel('Pf_low')
    plt.legend()
    plt.title('Probability Pf_low as a function of p')
    plt.show()

def plot_average_size_max_cluster():
    L = 10
    T = 20
    p_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    for p in p_values:
        filename = f'output/Ave-L{L}T{T}.txt'
        p_values, pf_low = read_ave_file(filename)
        plt.plot(p_values, pf_low, label=f'L={L}', marker='o')

    plt.xlabel('p')
    plt.ylabel('Pf_low')
    plt.legend()
    plt.title('Probability Pf_low as a function of p')
    plt.show()

def read_ave_output_file(filename):
    data = np.loadtxt(filename)
    p_values = data[:, 0]
    pf_low = data[:, 1]
    avg_smax = data[:, 2]
    return p_values, pf_low, avg_smax

def plot_avg_smax_vs_p():
    fig, ax = plt.subplots()
    L_values = [100]
    T = 20

    for L in L_values:
        filename = f'output/Ave-L{L}T{T}.txt'
        p_values, _, avg_smax = read_ave_output_file(filename)
        ax.plot(p_values, avg_smax, label=f'L={L}', marker='s')

    ax.set_xlabel('p')
    ax.set_ylabel('Average size of the maximum cluster ⟨smax⟩')
    ax.legend()
    ax.grid(True)
    plt.show()

# Generate the figures
# plot_sample_configurations()
# plot_pf_low_vs_p()
# plot_avg_smax_vs_p()
plot_avg_smax_vs_p()
# plot_p_flow_for_given_output()