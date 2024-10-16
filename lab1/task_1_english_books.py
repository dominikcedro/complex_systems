"""
author: Dominik Cedro
date: 06.10.2024
description: Complex systems, lab 1. This file contains my solutions to task1, finding the Zipf distribution in literature
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from icecream import ic

BOOK_TITLES_TASK_1 = [ # task with english books
        "moby_dick",
        "metamorphosis",
        "pride_and_prejudice",
        "the_great_gatsby"
    ]



def create_dfs_from_csvs(BOOK_TITLES):
    """
    Creates a list of DataFrames from CSV files based on the provided book titles.

    This function scans the './csv_output' directory for CSV files that match the titles
    in the BOOK_TITLES list. For each matching file, it reads the CSV into a DataFrame
    and appends it to a list.

    Args:
        BOOK_TITLES (list of str): A list of book titles to match against CSV filenames.

    Returns:
        list of pandas.DataFrame: A list of DataFrames corresponding to the matched CSV files.
    """
    dfs = []
    with os.scandir('./csv_output') as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                for title in BOOK_TITLES:
                    if title in entry.name:
                        df = pd.read_csv(entry.path)
                        dfs.append(df)
                        break
    return dfs


def calculate_theoritical_zipf(df):
    """
    Calculates the theoretical Zipf distribution for a given DataFrame.

    This function computes the theoretical Zipf distribution based on the length of the DataFrame.
    It returns the Zipf values and their corresponding ranks.

    Args:
        df (pandas.DataFrame): The DataFrame for which to calculate the Zipf distribution.

    Returns:
        tuple: A tuple containing:
            - zipf (numpy.ndarray): Theoretical Zipf distribution values.
            - ranks (numpy.ndarray): Corresponding ranks for the Zipf distribution.
    """
    N = len(df)
    ranks = np.arange(1, N + 1)
    zipf = 1 / ranks
    zipf /= zipf.sum()

    return zipf, ranks


def plot_zipf_save_plot(df, zipf, ranks, name_of_book):
    """
    Creates and saves a plot for the Zipf distribution.

    This function generates a plot comparing the empirical Zipf distribution from the DataFrame
    with the theoretical Zipf distribution. It creates both linear and log-log scale plots and
    saves the plot to a file.

    Args:
        df (pandas.DataFrame): The DataFrame containing the empirical Zipf distribution data.
        zipf (numpy.ndarray): Theoretical Zipf distribution values.
        ranks (numpy.ndarray): Corresponding ranks for the Zipf distribution.
        name_of_book (str): The name of the book, used for the plot title and filename.

    Returns:
        None
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    # linear
    ax1.scatter(df['rank'], df['freq'], label='Empirical', color='steelblue')
    ax1.plot(ranks, zipf, label='Theoretical Zipf', color='orange')
    ax1.set_xlabel('Rank')
    ax1.set_ylabel('Frequency')
    ax1.set_title(f'Empirical vs Theoretical Zipf Distribution (Linear Scale) for {name_of_book}')
    ax1.legend()

    # log log scale
    ax2.scatter(df['rank'], df['freq'], label='Empirical', color='steelblue')
    ax2.plot(ranks, zipf, label='Theoretical Zipf', color='orange')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Rank')
    ax2.set_ylabel('Frequency')
    ax2.set_title(f'Empirical vs Theoretical Zipf Distribution (Log-Log Scale) for {name_of_book}')
    ax2.legend()

    plt.tight_layout()
    plt.savefig(f'./plot_output/{name_of_book}')
    ic('Saved plot for ', name_of_book)
    return None


if __name__ == "__main__":
    list_dfs_task_1 = create_dfs_from_csvs(BOOK_TITLES_TASK_1)

    for df, book_title in zip(list_dfs_task_1, BOOK_TITLES_TASK_1):
        zipf, ranks = calculate_theoritical_zipf(df)
        plot_zipf_save_plot(df, zipf, ranks, book_title)