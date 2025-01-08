"""
author: Dominik Cedro
date: 08.12.2024
description: Main program for percolation laboratory list of tasks.
"""
import numpy as np
import random
import matplotlib.pyplot as plt
from icecream import ic

SIZE_OF_LATTICE = 15 # from the input file
site_p = 0.8 # probability of occupation of lattice site

def create_lattice(size_of_lattice, site_p):
    """

    :param size_of_lattice:
    :param site_p:
    :return: lattice: (np.array)
    """
    random_r = 0  # will be chosen randomly later on
    lattice = []
    random.seed(42)

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


def burning_method(lattice_raw):
    lattice = np.copy(lattice_raw)
    t_value = 2

    for index, site in enumerate(lattice[0]):
        if site == 1:
            lattice[0][index] = t_value

    for index in range(1, len(lattice)):
        t_value += 1
        row = lattice[index]
        row_above = lattice[index - 1]

        for site_index, site in enumerate(row):
            if row_above[site_index] >= 2 and site == 1:
                row[site_index] = t_value

        for site_index, site in enumerate(row):
            if site >= 2:
                if site_index > 0 and row[site_index - 1] == 1  and index<len(lattice)-1:  # check on the left
                    row[site_index - 1] = t_value
                if site_index < len(row) - 1 and row[site_index + 1] == 1 and index<len(lattice)-1:  # check right site
                    row[site_index + 1] = t_value
                if index < len(lattice) - 1 and lattice[index + 1][site_index] == 1:  # checking  below site
                    lattice[index + 1][site_index] = t_value

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

plot_lattice_with_values(lattice)
lattice_burning = burning_method(lattice)
plot_lattice_with_values(lattice_burning)
