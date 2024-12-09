"""
author: Dominik Cedro
date: 08.12.2024
description: Main program for percolation laboratory list of tasks.
"""
import numpy as np
import random
import matplotlib.pyplot as plt
from icecream import ic

# initiate the lattice

SIZE_OF_LATTICE = 30 # from the input file
site_p = 0.8 # probability of occupation of lattice site

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

lattice = create_lattice(SIZE_OF_LATTICE, site_p)
##### EXTRA - present lattice

def plot_lattice(lattice):
    plt.imshow(lattice, interpolation='none')
    plt.colorbar(label='Site Occupation')
    plt.title('Lattice Occupation')
    plt.xlabel('Column')
    plt.ylabel('Row')
    plt.show()

# plot_lattice(lattice)
plot_lattice(lattice)

##### BURNING METHOD

# now i will go over lattice copy
# for all top occupied i set their value to 2
# t += 1
# i go over the top line once again and check for neighbours (if index-1 or +1  == 1 or from above or below if  index equal is ==1

for index, site in enumerate(lattice[0]):
    if site == 1:
        lattice[0][index] = 2
print("")
# print(lattice)

t_value = 2
for index, row in enumerate(lattice):
    change = False

    t_value +=1
    # ic(t_value)
    # ic(index, row)
    if index == 0: # for the first row
        # only check south
        row_below = lattice[index+1]
        # ic(row_below)
        for site_index, site in enumerate(row):
            if row_below[site_index] == 1 and site == 2:
                # ic("below is one for", site, site_index)
                row_below[site_index] = t_value
    if index == len(lattice)-1: # for lat row
        row_above = lattice[index - 1]
        # ic(row_below)
        for site_index, site in enumerate(row):
            # termination statement

            if row_above[site_index] == 1 and site > 1:
                # ic("below is one for", site, site_index)
                row_above[site_index] = t_value
                change = True

            if  site > 1 and row[site_index - 1] == 1:  # check left
                row[site_index - 1] = t_value
                change = True

            if site_index != len(row) - 1 and site > 1 and row[site_index + 1] == 1:  # check right
                row[site_index + 1] = t_value
                change = True

    if index != len(lattice)-1: # change it to else: later because we are skipping last row
        row_below = lattice[index + 1]
        row_above = lattice[index - 1]
        # ic(row_below)
        for site_index, site in enumerate(row):
            # termination statement
            if row_above[site_index] == 1 and site > 1:
                # ic("below is one for", site, site_index)
                row_above[site_index] = t_value
                change = True
            if row_below[site_index] == 1 and site > 1:
                # ic("below is one for", site, site_index)
                row_below[site_index] = t_value
                change = True

            if site > 1 and row[site_index-1] == 1: # check left
                row[site_index - 1] = t_value
                change = True

            if site_index != len(row)-1 and site > 1 and row[site_index + 1] == 1: # check right
                row[site_index + 1] = t_value
                change = True
        if not change:
            ic("not changes made", change)
            break



plot_lattice(lattice)

# currently I have one issue with the results. because my algorithm searches
# from left to right there is a tendency to not reach to left side enough
# im thinking if applying the same algorithm but with other direction would work
#to fix this issue or maybe applying some regression to left side just to reach far enough?
