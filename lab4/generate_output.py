from collections import Counter

import numpy as np

from lab4.solution import read_input_parameters, create_lattice, burning_method, hoshen_kopelman, \
    write_ave_output_to_file, write_dist_output_to_file

if __name__ == "__main__":
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