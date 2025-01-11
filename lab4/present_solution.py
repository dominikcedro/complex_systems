"""
author: Dominik Cedro
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from icecream import ic
import lab4.solution as solution


def read_ave_output_file(filename):
    data = np.loadtxt(filename)
    p_values = data[:, 0]
    pf_low = data[:, 1]
    avg_smax = data[:, 2]
    return p_values, pf_low, avg_smax


def plot_cluster_distribution():
    fig, axs = plt.subplots(3, 3, figsize=(20, 20))
    p_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    for i, p in enumerate(p_values):
        filename = f'output/Dist-p{p}L10T1000.txt'
        sizes, counts = solution.read_dist_file(filename)
        # ic(len(sizes), len(counts))
        ax = axs[i // 3, i % 3]
        ax.plot(sizes, counts, label=f'p={p}', marker='^', linestyle='None')

        ax.set_xlabel('Cluster size [a.u]',fontsize=16)
        ax.set_ylabel('Cluster count [a.u]',fontsize=16)
        ax.legend(prop={'size':20})
        ax.grid(True)
    plt.tight_layout()
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.subplots_adjust(hspace=0.2)
    plt.subplots_adjust(wspace=0.2)

    fig.suptitle('Distribution of clusters for given p ', fontsize=25)
    plt.savefig(fname=f'plot/dist.png', format='png')
    plt.show()


def plot_p_flow_for_given_output(input_L=None): # TASK B
    if input_L:
        L_values = input_L
    else:
        L_values = [10, 50, 100]

    T = 1000

    for L in L_values:
        filename = f'output/Ave-L{L}T{T}.txt'
        p_values, pf_low = solution.read_ave_file(filename)
        plt.plot(p_values, pf_low, label=f'L={L}', marker='o', linestyle='dashed')

    plt.xlabel('p [a.u]')
    plt.ylabel('P_flow [a.u] ')
    plt.legend()
    plt.grid(True)
    plt.title('Probability Pf_low as a function of p')
    plt.savefig(fname=f'plot/p_flow.png', format='png')
    plt.show()


def plot_avg_smax_vs_p():
    fig, ax = plt.subplots()
    L_values = [10, 50, 100]
    T = 1000

    for L in L_values:
        filename = f'output/Ave-L{L}T{T}.txt'
        p_values, _, avg_smax = read_ave_output_file(filename)
        ax.plot(p_values, avg_smax, label=f'L={L}', marker='s')
    ax.set_xlabel('p [a.u]')
    ax.set_ylabel('Average size of the maximum cluster ⟨smax⟩ [a.u]')
    ax.legend()
    ax.grid(True)
    plt.title('Average size of the maximum cluster as a function of p')
    plt.savefig(fname=f'plot/_smax.png', format='png')
    plt.show()
