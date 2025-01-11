"""
author: Dominiik Cedro
description: Main module to generate solutions and plots for tasks a, b, c, d
"""
from icecream import ic
from lab4.solution import create_lattice, plot_lattice_with_values, burning_method
from lab4.present_solution import plot_p_flow_for_given_output, plot_avg_smax_vs_p, plot_cluster_distribution
from lab4.solution import hoshen_kopelman

if __name__ == "__main__":
    a = True # visualize sample configurations for L = 10 and 3 values of p
    b = True # probability p_flow
    c = True # average size of maximum cluster
    d = True # distribution of clusters
    L = [10, 50, 100]
    if a:
        lattice_size_ex1 = 10
        percolation_p_ex1 = [0.4, 0.6, 0.8]
        for p in percolation_p_ex1:
            lattice_raw = create_lattice(lattice_size_ex1, p, 10)
            plot_lattice_with_values(lattice_raw, file_name=f"Lattice raw {p}",plot_title='Initial lattice occupation', save=True)
            lattice_burning, connection = burning_method(lattice_raw)
            plot_lattice_with_values(lattice_burning, f"Burning method p={p}", plot_title='Burning Method algorithm results',save=True)
            labeled_lattice, cluster_sizes, max_size, distribution = hoshen_kopelman(lattice_raw)
            plot_lattice_with_values(labeled_lattice, save=True, file_name=f"Hoshen_Kopelman{p}", plot_title='Hoshen-Kopelman algorithm results')

    if b:
        plot_p_flow_for_given_output()

    if c:
        plot_avg_smax_vs_p()

    if d:
        plot_cluster_distribution()
