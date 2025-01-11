"""
author: Dominik Cedro
description: This file contains solution to generate output to /output/ folder
variables are loaded from 'perc_ini.txt' file.
"""
from collections import Counter
import numpy as np
from icecream import ic
import lab4.solution as solution
import time
import cProfile
import pstats


def main():
    params = solution.read_input_parameters('perc_ini.txt')
    L = int(params['L'])
    T = int(params['T'])
    p_0 = params['p0']
    p_k = params['pk']
    d_p = params['dp']
    p_flow = {}
    avg_smax = {}
    cluster_distribution = {}

    p_values = np.arange(p_0, p_k, d_p)
    for p in p_values:
        # ic(time.time())
        ic(p)
        pf_count = 0
        smax_total = 0
        distribution_total = Counter()

        for _ in range(1,T):
            # ic(_)
            lattice = solution.create_lattice(L, p)
            lattice_burned, connection = solution.burning_method(lattice)
            lattice_hoshen, cluster_sizes, max_cluster_size, distribution = solution.hoshen_kopelman(lattice)

            pf_count += connection

            smax_total += max_cluster_size
            distribution_total.update(distribution)

        p_flow[p] = pf_count / T
        avg_smax[p] = smax_total / T
        cluster_distribution[p] = dict(distribution_total)

    solution.write_ave_output_to_file(L, T, p_flow, avg_smax)
    solution.write_dist_output_to_file(L, T, cluster_distribution)


if __name__ == "__main__":
    # cProfile.run('main()', 'profile_output')
    # p = pstats.Stats('profile_output')
    # p.sort_stats('cumulative').print_stats(10)
    main()
