"""
author: Dominik Cedro
date: 08.12.2024
description: Main program for percolation laboratory list of tasks.
"""
import numpy as np
import random

from icecream import ic

# initiate the lattice

SIZE_OF_LATTICE = 10 # from the input file
site_p = 0.5 # probability of occupation of lattice site

def create_lattice(size_of_lattice, site_p):
    """

    :param size_of_lattice:
    :param site_p:
    :return: lattice: (np.array)
    """
    random_r = 0  # will be chosen randomly later on
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
    print(lattice)
    return lattice

create_lattice(SIZE_OF_LATTICE, site_p)

